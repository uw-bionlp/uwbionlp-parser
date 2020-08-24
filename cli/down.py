#!/usr/bin/env python3

import sys
from cli.utils import get_container_runtime, get_containers, run_shell_cmd

runtime = get_container_runtime()

def rm(ids):
    cmd = f'{runtime} rm {" ".join(ids)}'
    sys.stdout.write(f'{cmd}\n')
    run_shell_cmd(cmd)

def stop(ids):
    cmd = f'{runtime} stop {" ".join(ids)}'
    sys.stdout.write(f'{cmd}\n')
    run_shell_cmd(cmd)

def undeploy_containers():
    containers = [ container for key, container in get_containers().items() ]
    running = [ container for container in containers if container.up ]
    if len(running) > 0:
        stop([ container.id for container in running ])
    if len(containers) > 0:
        rm([ container.id for container in containers ])

if __name__ == '__main__':
    undeploy_containers()