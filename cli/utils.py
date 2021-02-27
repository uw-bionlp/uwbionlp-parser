import os
import sys
import subprocess
from cli.constants import *
from argparse import ArgumentError


class ContainerImage:
    def __init__(self, txt):
        splt = [ x for x in txt.split('  ') if x != '' ]
        self.id   = splt[2].strip()
        self.name = splt[0].strip()


class Container:
    def __init__(self, txt):
        splt = [ x for x in txt.split('  ') if x != '' ]
        self.id   = splt[0].strip()
        self.img  = splt[1].strip() if len(splt) > 1 else ''
        self.name = splt[-1].strip() if len(splt) > 1 else ''
        self.up   = False
        self.host = ''
        self.port = ''

        # COMMAND may be empty
        if len(splt) == 6:
            splt.insert(2, '')

        full_data = len(splt) == 7
        if len(splt) > 1:
            port_forwarding = '->' in splt[5]
            if full_data:
                self.up   = 'Up ' in splt[4]
            if port_forwarding:
                self.host = splt[5].split('->')[0].split(':')[0].strip()
                self.port = splt[5].split('->')[0].split(':')[1].strip()


def get_images():
    app = get_app_name()
    runtime = get_container_runtime()
    output = run_shell_cmd(f'{runtime} images')
    images = [ ContainerImage(img) for img in str(output).split('\\n') if app in img ]
    return { img.name : img for img in images }


def get_containers(app_only=True):
    app = get_app_name()
    runtime = get_container_runtime()
    output = run_shell_cmd(f'{runtime} ps -a')
    if app_only:
        containers = [ Container(cont) for cont in str(output).split('\\n') if app in cont ]
    else:
        containers = [ Container(cont) for cont in str(output).split('\\n') ]
    return { cont.name : cont for cont in containers }


def get_env_vars():
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
    if os.path.exists(dotenv_path):
        with open(dotenv_path, 'r') as f:
            dotenv_ls = [ l.strip().replace(' ','') for l in f if l.strip() and not l.startswith('#') ]
            dotenv_dict = dict([ l.split('=', 1) for l in dotenv_ls if '=' in l ])
    else:
        raise ArgumentError('A valid .env file was not found in your uwbionlp-parser directory. Exiting...')

    return dotenv_dict


def get_possible_ports(env_args):
    if 'PORTS' not in env_args:
        raise ArgumentError('An entry for `PORTS` was not found in your .env file. Exiting...')

    ports = []
    entries = env_args['PORTS'].split(',')
    for e in entries:
        if '-' in e:
            parts = e.split('-')
            if len(parts) == 2:
                e1, e2 = int(parts[0]), int(parts[1])
                for i in range(e1, e2):
                    ports.append(i)
            else:
                raise ArgumentError(f'Invalid `PORTS` entry in .env file: `{e}`. Range values should be of form `<integer>-<integer>`')
        else:
            ports.append(int(e))
    return ports
    

def get_env_var(name):
    dotenv_dict = get_env_vars()
    return dotenv_dict.get(name)


def get_container_runtime():
    cmds = [ 'podman', 'docker' ]
    for cmd in cmds:
        try:
            subprocess.call(f'{cmd} ps -a'.split(), stdout=subprocess.PIPE)
            return cmd
        except:
            pass
    sys.stdout.write(f'No usable container runtime (ie, `podman` or `docker`) found. Exiting.\n')
    sys.exit()


def run_shell_cmd(cmd, detach=False):
    try:
        if detach:
            pid = os.fork()
            if pid > 0:
                return
            os.setsid()
            pid = os.fork()
            if pid > 0:
                sys.exit(0)
            subprocess.call(cmd.split(), stdout=None, stderr=None)
            os._exit(os.EX_OK)
        else:
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
            return process.communicate()    
    except Exception as ex:
        sys.stdout.write(f'{ex}\n')
        return None, ex


def get_app_name():
    env = get_env_vars()
    if 'APP_NAME' in env:
        return env['APP_NAME'].lower()
    return APP_NAME