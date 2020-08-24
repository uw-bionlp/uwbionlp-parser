#!/usr/bin/env python3

import os
import sys
import grpc
import json
import queue
from pathlib import Path
from argparse import ArgumentParser
from time import localtime, strftime, sleep
from multiprocessing.dummy import Process, Queue, current_process
import threading

from cli.constants import *
from cli.utils import get_env_vars, get_containers
from cli.up import deploy_containers
from cli.down import undeploy_containers
from cli.clients.deident import DeidentificationChannelManager
from cli.clients.covid import CovidPredictorChannelManager
from cli.clients.sdoh import SdohPredictorChannelManager
from cli.clients.metamap import MetaMapChannelManager
from cli.clients.opennlp import OpenNLPChannelManager
from cli.clients.assertion_classifier import AssertionClassifierChannelManager

""" Globals """
lck = threading.Lock()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('file_or_dir', help='Absolute or relative path to the file or directory to parse.')
    parser.add_argument('--output_path', help='Directory or .jsonl file to write output to. Defaults to /output/<current_time>/')
    parser.add_argument('--output_type', help='Whether to write output to multiple files in a directory, "multi-file", or a single .jsonl file, "single-file"', default='multi-file', choices=['multi-file','single-file'])
    parser.add_argument('--threads', help='Number of threads with which to execute processing in parallel. Defaults to one.', default=1, type=int)
    parser.add_argument('--metamap', help='Whether to parse with MetaMap or not. Defaults to false.', default=False, dest='metamap', action='store_true')
    parser.add_argument('--metamap_semantic_types', help="MetaMap semantic types to include (eg, 'sosy', 'fndg'). Defaults to all.", nargs='+')
    parser.add_argument('--deident', help='Whether to predict named entity PHI elements and de-identify. Defaults to false.', default=False, dest='deident', action='store_true')
    parser.add_argument('--covid', help='Whether to predict with the COVID prediction algorithm or not. Defaults to false.', default=False, dest='covid', action='store_true')
    parser.add_argument('--sdoh', help='Whether to predict with the Social Determinants of Health prediction algorithm or not. Defaults to false.', default=False, dest='sdoh', action='store_true')
    parser.add_argument('--gpu', help='Integer indicating GPU id to use, if available. Defaults to -1.', default=-1, type=int)
    parser.add_argument('--batch-size', default=0, type=int)
    parser.add_argument('--verbose')
    # parser.add_argument('--brat', help='Output BRAT-format annotation files, in addition to JSON.', default=False, dest='brat', action='store_true')

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit()

    args.file_or_dir = os.path.abspath(args.file_or_dir)
    if not args.output_path:
        args.output_path = os.path.join(os.getcwd(), 'output', f'{Path(args.file_or_dir).stem}_{strftime("%Y%m%d-%H%M%S")}')
    if args.output_type == 'single-file':
        args.output_path = args.output_path + '.jsonl'

    # Until memory-leak(?) is fixed, auto-batch metamap by magic number
    if args.metamap:
        args.batch_size = args.threads * 130
    
    return args


def write_output(output, args):
    """ Write output to directory or .jsonl file in pretty-printed JSON. """

    filename = output['id']
    if args.output_type == 'single-file':
        with open(args.output_path, 'a+') as f:
            f.write(json.dumps(output, ensure_ascii=False) + '\n')
    else:
        with open(os.path.join(args.output_path, filename + '.json'), 'w') as f:
            json.dump(output, f, ensure_ascii=False, indent=4)


def setup_containers(args):
    envs = get_env_vars()
    envport_else_default = lambda name, default: int(envs[name.upper()+'_PORT']) if name.upper()+'_PORT' in envs else int(default)
    added = []

    deploy_containers(OPENNLP, envport_else_default(OPENNLP, OPENNLP_PORT))
    if args.metamap: added += deploy_containers(METAMAP, envport_else_default(METAMAP, METAMAP_PORT), args.threads)
    if args.covid:   added += deploy_containers(COVID, envport_else_default(COVID, COVID_PORT), args.threads)
    if args.sdoh:    added += deploy_containers(SDOH, envport_else_default(SDOH, SDOH_PORT), args.threads)
    if args.deident: added += deploy_containers(DEIDENT, envport_else_default(DEIDENT, DEIDENT_PORT), args.threads)

    if len(added):
        wait_seconds = 30
        print(f'Waiting {wait_seconds} seconds for container interfaces to load...')
        sleep(wait_seconds)

    return get_containers()


def get_channels(containers, args):
    channel_groups = []
    available_containers = {}
    algos = []
    
    if args.metamap: algos.append(( METAMAP, MetaMapChannelManager ))
    if args.covid:   algos.append(( COVID, CovidPredictorChannelManager ))
    if args.sdoh:    algos.append(( SDOH, SdohPredictorChannelManager ))
    if args.deident: algos.append(( DEIDENT, DeidentificationChannelManager ))

    # Gather containers for each algorithm
    for name, channel_manager in algos:
        available_containers[name] = [ container for key, container in containers.items() if name in container.name ]

    # Add a channel group for each thread
    for thread in range(args.threads):
        channel_group = []
        for name, channel_manager in algos:
            container = available_containers[name][thread]
            channel_group.append(channel_manager(container))
        channel_groups.append(channel_group)
    
    # Pull out OpenNLP, as that will only ever have one container 
    opennlp_container = [ container for key, container in containers.items() if OPENNLP in container.name ][0]
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
        print(f'Processing document "{doc}"... by thread {thread_idx}')
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


def main():
    """ Run the client. """

    # Parse args, bail if invalid.
    args = parse_args()
    if not os.path.exists(args.file_or_dir):
        print(f"The file or directory '{args.file_or_dir}' could not be found!\n")
        return

    # Make output directory.
    Path(args.output_path).mkdir(parents=True, exist_ok=True)

    # Load documents
    if os.path.isfile(args.file_or_dir):
        files = [ args.file_or_dir ]
    else:
        files = [ f'{args.file_or_dir}{os.path.sep}{f}' for f in os.listdir(args.file_or_dir) if Path(f).suffix == '.txt' ]
        print(f"Found {len(files)} text files in '{args.file_or_dir}'...")

    # Batch files
    batches = batch_files(files, args)

    try:
        for batch in batches:

            # Fire up containers, one for each requested thread per algorithm
            containers = setup_containers(args) 

            # Get and open gRPC channels.
            opennlp_channel, channel_groups = get_channels(containers, args)
            opennlp_channel.open()
            for channel_group in channel_groups: 
                for channel in channel_group: 
                    channel.open()

            # Process multithread.
            remaining = Queue()
            completed = Queue()
            processes = []
            for f in batch: 
                remaining.put(f)

            # Spin up a subprocess for each requested thread.
            for i, channel_group in enumerate(channel_groups, 1):
                p = Process(target=do_subprocess, args=(remaining, completed, args, opennlp_channel, channel_group, i))
                processes.append(p)
                p.start()
            for p in processes:
                p.join()

            # Close all gRPC channels.
            opennlp_channel.close()
            for channel_group in channel_groups:
                for channel in channel_group:
                    channel.close()

            # Undeploy containers.
            undeploy_containers()

        print(f"All done! Results written to '{args.output_path}'") 

    except Exception as ex:
        print(f"An error occurred: '{ex}'. Exiting...")
        undeploy_containers()
        sys.exit()


if __name__ == '__main__':
    main()