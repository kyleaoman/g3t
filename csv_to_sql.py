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
    parser.add_argument('--outfile', type=str,help='outputgile', required=True)
    parser.add_argument('--map',type=str, nargs='+',default=[])
    args = parser.parse_args()
    for k in args.__dict__:
        printf("%s %s\n"%(k,str(args.__dict__[k])),e=True)

    header=None
    rows=[]
    with open(args.outfile,'r') as f:
        row={}
        for line in f:
            if line[0]=='#':
                if header is None:
                    header=line.split()
                    header[0]=header[0][1:] #remove hash at beginning of haeader line
            else:
                fields = line.split()
                for ikey in range(len(header)):
                    row[key] = 
            
    args.outfile = args.outfile+'.'+str(args.chunk)
    last_id_cluster = None

    if  args.restart and os.path.isfile(args.outfile):
        last_line=None
        with open(args.outfile, 'r') as fd:
            for line in fd:
                last_line=line
        if last_line is not None:
            last_id_cluster = int(last_line.split()[0])
    else:
        with open(args.outfile,'w') as fd:
            pass
        

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
    n_fofs_db = FoF.select().where(FoF.snap==snap).count()
    page_size = n_fofs_db//(args.chunks-1)
    printf("Chunk%d N FoFs in snap database: %d\n"%(args.chunk, n_fofs_db),e=True)
    page = FoF.select().where(FoF.snap==snap).order_by(FoF.id_cluster.asc()).paginate(args.chunk+1, page_size)

    shown_keys=False
    keys={}
    for db_fof in page:
        db_fof_id = db_fof.id
        ifile  = db_fof.i_file
        ifof = db_fof.id_cluster
        if args.restart and last_id_cluster is not None and ifof<last_id_cluster:
            printf("Skip ifof %d\n"%(ifof),e=True)
            continue
        cluster_data = pp.PostProcessing(
                cluster_id=ifof,
                cluster_id_in_file=db_fof.i_in_file,
                cluster_i_file=ifile,
                group_base = args.basegroup,
                snap_base = args.basesnap,
                subfind_and_fof_same_file=False,
                subfind_files_range=[db_fof.start_subfind_file, db_fof.end_subfind_file]
            )
        with open(args.outfile,'a') as fd:
            reses={}
            for prop in args.props:
                if prop == "fossilness": res = cluster_data.fossilness()
                elif prop ==  "virialness": res = cluster_data.virialness()
                elif prop ==  "c200c": res = cluster_data.c200c()
                else: raise Exception("property %s not found"%prop)
                reses[prop]=res
                
            if shown_keys == False:
                    printf("#id_Cluster ")
                    if last_id_cluster is None: printf("#id_Cluster ",fd=fd)
                    for prop in args.props:
                        res=reses[prop]
                        if isprimitive(res):
                            printf("%s "%prop)
                            if last_id_cluster is None: printf("%s "%prop,fd=fd)
                        else:
                            keys[prop]=[]
                            for k in sorted(res.__dict__): #everytime get same order :)
                                keys[prop].append(k)
                            printf("%s "%(' '.join(map(lambda x: prop+'_'+x, keys[prop]))))
                            if last_id_cluster is None: printf("%s "%(' '.join(map(lambda x: prop+'_'+x, keys[prop]))),fd=fd)

                    printf("\n")
                    if last_id_cluster is None: printf("\n",fd=fd)

            shown_keys=True
            printf("%d "%(ifof))
            printf("%d "%(ifof),fd=fd)
            for prop in args.props:
                res=reses[prop]
                if isprimitive(res):
                    printf("%s "%(str(res)))
                    printf("%s "%(str(res)),fd=fd)
                else:
                    for k in keys[prop]:
                        printf("%s "%(str(res.__dict__[k])))
                        printf("%s "%(str(res.__dict__[k])),fd=fd)
                   
            printf("\n")
            printf("\n",fd=fd)


if __name__ == "__main__": 
    main()
    sys.exit(0)
