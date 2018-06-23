#!/usr/bin/python
import pp
from pp_schema  import *
import g3read as g
#g.debug=True
import numpy as np
import sys
import logging
import numpy as np
import argparse
import os

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
def isprimitive(value):
  return not hasattr(value, '__dict__') 
def main():
    import numpy as np
    import json
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--simulation-name', type=str,help='name of simulation', required=True)
    parser.add_argument('--snap', type=str,help='snap___', required=True)
    parser.add_argument('--outfile', type=str,help='outputgile', nargs='+', required=True)
    parser.add_argument('--map',type=str, nargs='+',default=[])
    args = parser.parse_args()
    for k in args.__dict__:
        printf("%s %s\n"%(k,str(args.__dict__[k])),e=True)

    header=None
    rows=[]

    simulation = Simulation.get_or_none(name=args.simulation_name)
    if simulation is None:
        printf("No snap found with name=%s. List:\n"%(args.simulation_name),e=True)
        sims = Simulation.select()
        for sim in sims:
            printf("Name: %s\n"%(sim.name),e=True)
        sys.exit(1)

    snap = simulation.snaps.where(Snap.name==args.snap).first()
    if snap is None:
        printf("No snap found with name=%s\n"%(args.snap))
        sys.exit(1)
    conv={}
    for mappa in args.map:
        chiave,valore = mappa.split('=')
        conv[chiave]=valore

    snap_id = str(snap.id)    
    iq=-1
    append_rows=[]
    for outfile in args.outfile:
        with open(outfile,'r') as f:
            for line in f:
                row={}
                row_strs=[]
                if line[0]=='#':
                    if header is None:
                        header=line.split()
                        header[0]=header[0][1:] #remove hash at beginning of haeader line
                else:
                    fields = line.split()
                    id_cluster=fields[0]
                    for ikey in range(1, len(header)):
                        key = header[ikey]
                        rkey = key
                        if key in conv:
                            rkey = conv[key]
                        row[rkey] = fields[ikey]
                        row_strs.append(' %s=%s '%(rkey, fields[ikey]))
                    row_str = 'AND'.join(row_strs)
                    q = "UPDATE FoF SET %s WHERE id_cluster = %s and snap_id=%s\n"%(row_str,id_cluster,snap_id)
                    append_rows.append(q)
                    #printf(q)
                    iq=iq+1
                    try:
                        if iq%10==0:
                            db.execute_sql(''.join(append_rows))
                            append_rows=[]
                    except Exception as e:
                        printf(''.join(append_rows),e=True)
                        raise Exception(e)

                    if iq%10==0: 
                        print("Done %d queries"%(iq))

if __name__ == "__main__": 
    main()
    sys.exit(0)
