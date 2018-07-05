#!/usr/bin/python
import sys
import g3read
import h5py
import argparse
import numpy as np

PY3 = sys.version_info[0] == 3

def printf(s,e=False,fd=None):
    if fd is None:
        fd=sys.stderr if e else sys.stdout
    fd.write(s)

def main():
    printf(" \n",e=True)
    printf(" (Open)gadget2+3 to HDF5 format \n",e=True)
    printf(" by Antonio Ragagnin, 2018\n",e=True)
    printf(" \n",e=True)
    printf(" usage: python gadget_to_hdf5.py -i infile -o outfile -p ptype -b block -n hdf5-name\n",e=True)
    printf(" example: python gadget_to_hdf5.py -i infile -o file.hdf5 -p 0 -b TEMP -n Temperature\n",e=True)
    printf(" \n",e=True)

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', type=str, required=True)
    parser.add_argument('-o', type=str, required=True)
    parser.add_argument('-p', type=int, required=True)
    parser.add_argument('-b', type=str, required=True)
    parser.add_argument('-n', type=str, required=True)

    args = parser.parse_args()
    

    ptype=args.p
        
    f = g3read.GadgetFile(args.i)
    with h5py.File(args.o, "w") as g:
        poses = f.read("POS ",ptype)
        g.create_dataset("X", data = poses[:,0])
        g.create_dataset("Y", data = poses[:,1])
        g.create_dataset("Z", data = poses[:,2])
        s=f.read(args.b,ptype)
        print("%s min=%f max=%f\n"%(args.b,np.min(s), np.max(s)))
        g.create_dataset(args.n, data = s)
        

if __name__ == "__main__":
    main()
#sys.argv[1], sys.argv[2])

