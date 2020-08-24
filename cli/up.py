#!/usr/bin/env python3

import sys
import time
import subprocess
from cli.utils import get_container_runtime, get_env_vars, get_images, get_containers, run_shell_cmd
from cli.constants import *

runtime = get_container_runtime()

def build(img_name, path):
    cmd = f'{runtime} build -t {img_name} -f {path}/Dockerfile {path}/'
    sys.stdout.write(f'{cmd}\n')
    run_shell_cmd(cmd)

def run(name, img_name, bind_port_to):

    # TODO(ndobb) Make additional params a property of clients.
    ipc_host = '--ipc=host' if ('covid' in img_name or 'sdoh' in img_name) else ''

    cmd = f'{runtime} run -d --name={name} -p {bind_port_to}:8080 {ipc_host} {img_name}'
    sys.stdout.write(f'{cmd}\n')

    # TODO(ndobb) Figure out why this is necessary.
    # If linux, run command as child process
    run_as_child_proc = sys.platform == 'linux'

    run_shell_cmd(cmd, run_as_child_proc) 

def wait_till_up(name, port):
    wait_cnt = 0
    wait_seconds = 2
    time.sleep(wait_seconds)
    up = False
    while not up:
        container = get_containers().get(name)
        up = container.up if container else False
        if not up:
            time.sleep(wait_seconds)
            wait_cnt += 1
            if wait_cnt >= 10:
                print(f'An error likely occurred while waiting for deployment of container: {name}. Are you sure port {port} is available?')
                sys.exit()

def deploy_containers(algorithm_name, port, desired_inst_cnt=1):
    images = [ img for key, img in get_images().items() ]
    containers = [ container for key, container in get_containers().items() ]
    img_name = f'{APP_NAME}_{algorithm_name}'
    added_container_names = []

    if not any([ x for x in images if img_name in x.name ]):
        build(img_name, algorithm_name)
    
    for i in range(desired_inst_cnt):
        cont_name = f'{APP_NAME}_{algorithm_name}_{i+1}'
        if not any([ x for x in containers if cont_name in x.name ]):
            run(cont_name, img_name, port)
            wait_till_up(cont_name, port)
            added_container_names.append(cont_name)
        port += 1

    return added_container_names

    # Clear dangling PIDs
    #cmd = "ps x | grep './up.sh' | awk '{print $1}' | xargs kill -9"
    #run_shell_cmd(cmd)
    #pids = [ l.strip().split(' ')[0] for l in str(run_shell_cmd('ps x')[0]).split('\\n') if './up.sh' in l and 'python3' in l ]
    #for p in pids:
    #    print(f'kill -9 {p}')
    #    run_shell_cmd(f'kill -9 {p}')