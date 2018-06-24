#!/usr/bin/python
import sys
import argparse
import tempfile
import shutil
import os

PY3 = sys.version_info[0] == 3


def printf(s,e=False,fd=None):
    if fd is None:
        fd=sys.stderr if e else sys.stdout
    fd.write(s)

def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value yes/true/t/y/1/no/false/f/n/0 expected. Got:%s '%v)

def main():
    import numpy as np
    import json
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-s', type=str, help='batch system, e.g. llsubmit or sbatch', default='llsubmit')
    parser.add_argument('-p', type=str, nargs='+', help='job paramas', default=[])
    parser.add_argument('-f', type=str, help='job file template. append the command at the end of the file', required=True)

    #args = parser.parse_args()
    args, unknownargs = parser.parse_known_args()

    if len(args.p)>0:
        raise Error("-p not implemented yet :(")

    fd = tempfile.NamedTemporaryFile(delete=False)
    fd.close()
    shutil.copyfile(args.f,fd.name)

    with open(fd.name,'a') as f:
        f.write(' '.join(unknownargs)+'\n')


    os.system('%s %s'%(args.s,fd.name))


if __name__ == "__main__":
    main()

