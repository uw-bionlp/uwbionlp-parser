#!/usr/bin/env python3

import sys
from cli.utils import get_container_runtime, get_images, run_shell_cmd

runtime = get_container_runtime()

def rm(ids):
    cmd = f'{runtime} rmi {" ".join(ids)}'
    sys.stdout.write(f'{cmd}\n')
    run_shell_cmd(cmd)

def main():
    images = get_images()
    if len(images) > 0:
        rm([ img.id for key,img in images.items() ])
    
    cmd = f"{runtime} images --filter label=stage=builder | grep '<none>' | " + "awk '{print $3}'" + f" | xargs {runtime} rmi"
    #run_shell_cmd(cmd)

if __name__ == '__main__':
    main()