#!/bin/sh
"exec" "`dirname $0`/venv/bin/python3" "$0" "$@"

import os
import sys
import json
import queue
import atexit
import threading
import traceback
from pathlib import Path
from pprint import pprint
from argparse import ArgumentParser
from time import strftime, sleep, time
from multiprocessing.dummy import Process, Queue

from cli.constants import *
from cli.utils import get_env_vars, get_containers, get_possible_ports
from cli.up import deploy_containers
from cli.down import undeploy_containers
from cli.clients.deident import DeidentificationChannelManager
from cli.clients.covid import CovidPredictorChannelManager
from cli.clients.sdoh import SdohPredictorChannelManager
from cli.clients.metamap import MetaMapChannelManager, semantic_types
from cli.clients.opennlp import OpenNLPChannelManager


""" Globals """
lck = threading.Lock()
running = False


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file_or_dir', help='Absolute or relative path to the file or directory to parse.')
    parser.add_argument('--output_path', help='Directory or .jsonl file to write output to. Defaults to /output/<current_time>/')
    parser.add_argument('--output_single_file', help='Write output to a single .jsonl file with one line per document output', default=False, dest='output_single_file', action='store_true')
    parser.add_argument('--threads', help='Number of threads with which to execute processing in parallel.', default=1, type=int)
    parser.add_argument('--metamap', help='Whether to parse with MetaMap or not.', default=False, dest='metamap', action='store_true')
    parser.add_argument('--metamap_semantic_types', help="MetaMap semantic types to include separated by spaces. Use like `--metamap_semantic_types dysn sosy`. Allowed values are "+', '.join(semantic_types) +".\n Defaults to all.", nargs='+')
    parser.add_argument('--deident', help='Whether to predict named entity PHI elements and de-identify.', default=False, dest='deident', action='store_true')
    parser.add_argument('--covid', help='Whether to predict with the COVID prediction algorithm or not.', default=False, dest='covid', action='store_true')
    parser.add_argument('--sdoh', help='Whether to predict with the Social Determinants of Health prediction algorithm or not.', default=False, dest='sdoh', action='store_true')
    parser.add_argument('--sdoh_mspert', help='Whether to predict with the SDOH mSpERT model or not.', default=False, dest='sdoh_mspert', action='store_true')
    parser.add_argument('--gpu', help='Integer indicating GPU id to use, if available.', default=-1, type=int)
    parser.add_argument('--batch_size', help='Frequency relative to documents processed with which to stop, remove, and re-run new containers during processing.', default=100, type=int)

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    args.file_or_dir = os.path.abspath(args.file_or_dir)
    if not args.output_path:
        args.output_path = os.path.join(os.path.dirname(__file__), 'output', f'{Path(args.file_or_dir).stem}_{strftime("%Y%m%d-%H%M%S")}')

    if args.metamap_semantic_types:
        invalid_types = [ tp for tp in args.metamap_semantic_types if tp not in semantic_types ]
        if any(invalid_types):
            print(f'The following semantic types are invalid: {" ".join(invalid_types)}')
            print(f'Valid semantic types are: {", ".join(semantic_types)}')
            print('Please verify your semantic types of interest and try again')
            sys.exit()

    print('Starting up parser. Params:')
    pprint(vars(args))
    print(f"Data will be output to '{args.output_path}'")

    return args


def write_output(output, args):
    """ Write output to directory or .jsonl file in pretty-printed JSON """

    filename = output['id']

    # Single .jsonl file
    if args.output_single_file:
        filename = os.path.join(args.output_path, 'output.jsonl')
        if not os.path.exists(filename):
            with open(filename, 'w+') as f: f.write('')
        with open(filename, 'a+') as f:
            f.write(json.dumps(output) + '\n')

    # One .json file per document
    else:
        with open(os.path.join(args.output_path, filename + '.json'), 'w') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)


def setup_containers(args):
    envs               = get_env_vars()
    running_containers = get_containers(app_only=False)
    possible_ports     = get_possible_ports(envs)
    used_ports         = [ int(c.port) for _,c in running_containers.items() if c.port and c.port.isnumeric() ]
    available_ports    = [ p for p in possible_ports if p not in used_ports ]
    added = []

    def provision_ports(thread_cnt):
        nonlocal available_ports
        threads = available_ports[:thread_cnt] 
        available_ports = [ p for p in available_ports if p not in threads ]
        return threads

    deploy_containers(OPENNLP, provision_ports(1))
    if args.metamap:     added += deploy_containers(METAMAP,     provision_ports(args.threads))
    if args.covid:       added += deploy_containers(COVID,       provision_ports(args.threads))
    if args.sdoh:        added += deploy_containers(SDOH,        provision_ports(args.threads))
    if args.sdoh_mspert: added += deploy_containers(SDOH_MSPERT, provision_ports(args.threads))
    if args.deident:     added += deploy_containers(DEIDENT,     provision_ports(args.threads))

    wait_seconds = 30
    print(f'Waiting {wait_seconds} seconds for container interfaces to load...')
    sleep(wait_seconds)

    return get_containers()


def get_channels(containers, args):
    channel_groups = []
    available_containers = {}
    algos = []
    
    if args.metamap:     algos.append(( METAMAP, MetaMapChannelManager ))
    if args.covid:       algos.append(( COVID,   CovidPredictorChannelManager ))
    if args.sdoh:        algos.append(( SDOH,    SdohPredictorChannelManager ))
    if args.sdoh_mspert: algos.append(( SDOH_MSPERT, SdohPredictorChannelManager ))
    if args.deident:     algos.append(( DEIDENT, DeidentificationChannelManager ))

    # Gather containers for each algorithm
    for name, channel_manager in algos:
        available_containers[name] = [ container for _, container in containers.items() if name in container.name ]

    # Add a channel group for each thread
    for thread in range(args.threads):
        channel_group = []
        for name, channel_manager in algos:
            container = available_containers[name][thread]
            channel_group.append(channel_manager(container))
        channel_groups.append(channel_group)
    
    # Pull out OpenNLP, as that will only ever have one container 
    opennlp_container = [ container for _, container in containers.items() if OPENNLP in container.name ][0]
    opennlp_channel = OpenNLPChannelManager(opennlp_container)

    return opennlp_channel, channel_groups


def process_doc(filepath, opennlp_client, clients, args):
    with open(filepath, 'r') as f:
        text = f.read()
        doc_id = Path(filepath).stem

    # Get base sentences, locking opennlp between threads.
    global lck
    lck.acquire()
    doc = opennlp_client.process(doc_id, text)
    json = opennlp_client.to_dict(doc)
    lck.release()

    # For each gRPC client, process file.
    for client in clients:
        response = client.process(doc)
        client_json = client.to_dict(response)
        json = client.merge(json, client_json)

    write_output(json, args)


def do_subprocess(remaining, completed, args, opennlp_channel, channels, thread_idx):
    
    # Get gRPC clients.
    clients = [ channel.generate_client(args) for channel in channels ]
    opennlp_client = opennlp_channel.generate_client()
    errored, error_limit, succeeded = 0, 10, 1

    while True:
        try:
            doc = remaining.get_nowait()
        except queue.Empty:
            break
        print(f"Processing document '{Path(doc).name}' by thread {thread_idx}")
        try:
            process_doc(doc, opennlp_client, clients, args)
            completed.put(doc)
            succeeded += 1
        except Exception as ex:
            errored += 1

            # If only run a handful of times, continue trying.
            if errored < error_limit:
                remaining.put(doc)
                print(f'"{doc}" failed. Error: "{ex}". Retrying...')
                continue

            print(f'{errored} documents failed, not retrying "{doc}"...')
            print(f'Error: {ex}')
            
    return True


def batch_files(files, args):
    if args.batch_size == 0:
        return [ files ]

    batches, curr_batch, i, files_len = [], [], 0, len(files)
    while i < files_len:
        curr_batch.append(files[i])
        if len(curr_batch) == args.batch_size:
            batches.append(curr_batch)
            curr_batch = []
        i += 1
    if len(curr_batch):
        batches.append(curr_batch)
    return batches


def undeploy_at_exit():
    if running:
        undeploy_containers()
        sys.exit()


def main():
    """ Run the client """
    global running 

    # Parse args, bail if invalid
    args = parse_args()
    if not os.path.exists(args.file_or_dir):
        print(f"The file or directory '{args.file_or_dir}' could not be found!\n")
        return

    # Make output directory
    if not os.path.exists(args.output_path):
        Path(args.output_path).mkdir(parents=True)

    # Load documents
    if os.path.isfile(args.file_or_dir):
        files = [ args.file_or_dir ]
        print(f"Found 1 text file '{args.file_or_dir}'...")
    else:
        files = [ os.path.join(args.file_or_dir, f) for f in os.listdir(args.file_or_dir) if Path(f).suffix == '.txt' ]
        print(f"Found {len(files)} text file(s) in '{args.file_or_dir}'")

    existing_files = set([ f for f in os.listdir(args.output_path) if f.split('.')[-1] == 'json' ])
    if any(existing_files) and not args.output_single_file:
        splitter = lambda x: x.split(os.path.sep)[-1].replace('.txt','.json')
        overlap = set([ f for f in files if splitter(f) in existing_files ])
        if any(overlap):
            print(f"Found {len(existing_files)} existing json files, these will be skipped")       
            files = [ f for f in files if f not in overlap ]

    if not any(files):
        print(f"There are no files to process!")  
        sys.exit()

    # Batch files
    batches = batch_files(files, args)
    running = True

    try:
        for batch in batches:

            # Fire up containers, one for each requested thread per algorithm
            containers = setup_containers(args)

            # Get and open gRPC channels
            opennlp_channel, channel_groups = get_channels(containers, args)
            opennlp_channel.open()
            for channel_group in channel_groups: 
                for channel in channel_group: 
                    channel.open()

            # Process multithread
            remaining = Queue()
            completed = Queue()
            processes = []
            for f in batch: 
                remaining.put(f)

            start_time = time()

            # Spin up a subprocess for each requested thread
            for i, channel_group in enumerate(channel_groups, 1):
                p = Process(target=do_subprocess, args=(remaining, completed, args, opennlp_channel, channel_group, i))
                processes.append(p)
                p.start()
            for p in processes:
                p.join()

            end_time = time() - start_time

            # Close all gRPC channels
            opennlp_channel.close()
            for channel_group in channel_groups:
                for channel in channel_group:
                    channel.close()

            # Undeploy containers
            undeploy_containers()

        print(f"All done! Processing completed in {round(end_time, 1)} seconds") 
        print(f"Results written to '{args.output_path}'") 

    except KeyboardInterrupt as ex:
        print(f"Cancelling job and undeploying containers")
        undeploy_at_exit()

    except Exception as ex:
        print(f"Unexpected exception occurred")
        traceback.print_exc()
        print(f"Cancelling job and undeploying containers")
        undeploy_at_exit()


atexit.register(undeploy_at_exit)
if __name__ == '__main__':
    main()