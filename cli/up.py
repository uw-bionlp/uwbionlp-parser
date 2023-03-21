import os
import sys
import time
from getpass import getuser
from cli.utils import get_container_runtime, get_images, get_containers, run_shell_cmd, get_app_name, get_root_path
from cli.constants import *

try:
    from pwd import getpwnam
    user = getuser()
    uid = getpwnam(user).pw_uid
except:
    user = None
    uid = None

runtime = get_container_runtime()


def build(img_name, path):
    path_ = os.path.join(get_root_path(), path)
    cmd = f'{runtime} build -t {img_name} -f {path_}/Dockerfile {path_}/'
    sys.stdout.write(f'{cmd}\n')
    run_shell_cmd(cmd)


def run(name, img_name, bind_port_to):
    run_as_child_proc = False #sys.platform == 'linux'
    ipc_host = 'covid' in img_name or 'sdoh' in img_name

    params = [ '-d', f'--name={name}', f'-p {bind_port_to}:8080' ]
    if uid      : params.append(f'--user={uid}')
    if ipc_host : params.append('--ipc=host')

    cmd = f'{runtime} run {" ".join(params)} {img_name}'
    sys.stdout.write(f'{cmd}\n')

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
                sys.stdout.write(f'An error likely occurred while waiting for deployment of container: {name}. Ending process!\n')
                sys.exit()


def deploy_containers(algorithm_name, ports):
    app = get_app_name()
    images = [ img for _, img in get_images().items() ]
    containers = [ container for _, container in get_containers().items() ]
    img_name = f'{app}_{algorithm_name}'
    added_container_names = []

    if not any([ x for x in images if img_name in x.name ]):
        build(img_name, algorithm_name)

    for p_i, port in enumerate(ports, 1):
        cont_name = f'{app}_{(user if user else port)}_{algorithm_name}_{p_i}'
        if not any([ x for x in containers if cont_name in x.name ]):
            run(cont_name, img_name, port)
            wait_till_up(cont_name, port)
            added_container_names.append(cont_name)

    return added_container_names