#!/usr/bin/python
import pp
from pp_schema  import *
import g3read as g
import numpy

def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)


def main():
    import argparse
    import numpy as np
    import json
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--basename', type=str, help='base file name of groups')
    parser.add_argument('--simulation-name', type=str,help='name of simulation')
    parser.add_argument('--tag', type=str,help='tag for snapshot')
    parser.add_argument('--snap', type=str,help='tag for snapshot')
    parser.add_argument('--min-glen', type=int,help='glen to stop',default=1e3)
    parser.add_argument('--min-mcri', type=int,help='mcri to stop in units of (1e10Msun/h)')
    parser.add_argument('--min-val', type=int,help='output')
    args = parser.parse_args()
    

    
    basegroup = args.basename+'groups_%s/sub_%s.'%(args.snap,args.snap)
    first_filename = basegroup+'0'
    first_file = g.GadgetFile(first_filename, is_snap=False)
    header = first_file.header
    nfiles = header.num_files        
    redshift = header.redshift
    a = 1./(1.+redshift)

    simulation = Simulation.get_or_create(name=args.simulation_name)
    simulation.redshift = redshift
    simulation.a = a
    simulation.path = args.basename
    simulation.save()
    

if __name__ == "__main__": main()
