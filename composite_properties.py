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


def printf(s,e=False):
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
    parser.add_argument('--basegroup', type=str, help='base file name of groups')
    parser.add_argument('--basesnap', type=str, help='base file name of snaps')
    parser.add_argument('--simulation-name', type=str,help='name of simulation')
    parser.add_argument('--tag', type=str,help='tag for snapshot')
    parser.add_argument('--snap', type=str,help='snap___')

    parser.add_argument('--chunk', type=int)
    parser.add_argument('--chunks', type=int)


    parser.add_argument('--prop', type=str)
    args = parser.parse_args()
    for k in args.__dict__:
        print(k,args.__dict__[k])


    simulation = Simulation.get_or_none(name=args.simulation_name)
    snap = simulation.snaps.where(Snap.name==args.snap).first()
    if snap is None:
        printf("No snap found with name=%s\n"%(args.snap))
        sys.exit(1)
    n_fofs_db = FoF.select().where(FoF.snap==snap).count()
    page_size = n_fofs_db//(args.chunks-1)
    printf("Chunk%d N FoFs in snap database: %d\n"%(args.chunk, n_fofs_db),e=True)
    page = FoF.select().where(FoF.snap==snap).order_by(FoF.id_cluster.asc()).paginate(args.chunk+1, page_size)

    shown_keys=False
    keys=[]
    for db_fof in page:
        db_fof_id = db_fof.id
        ifile  = db_fof.i_file
        ifof = db_fof.id_cluster
        #printf("Chunk%d FoF db-id: %d id_cluster:%d\n"%(args.chunk, db_fof_id,ifof),e=True)
        cluster_data = pp.PostProcessing(
                cluster_id=ifof,
                cluster_id_in_file=db_fof.i_in_file,
                cluster_i_file=ifile,
                group_base = args.basegroup,
                snap_base = args.basesnap,
                subfind_and_fof_same_file=False,
                subfind_files_range=[db_fof.start_subfind_file, db_fof.end_subfind_file]
            )

        for prop in [args.prop]:
            if prop == "fossilness": res = cluster_data.fossilness()
            elif prop ==  "virialness": res = cluster_data.virialness()
            elif prop ==  "c200c": res = cluster_data.c200c()
            else: raise Exception("property %s not found"%prop)
            
            if shown_keys == False:
                if not isprimitive(res):
                    for k in res.__dict__:
                            keys.append(k)
                    printf("#id_Cluster %s\n"%(' '.join(map(lambda x: prop+'_'+x, keys))))
                else:
                    printf("#id_Cluster %s\n"%prop)
                shown_keys=True
            printf("%d "%(ifof))
            if not isprimitive(res):
                for k in keys:
                    printf("%s "%(str(res.__dict__[k])))
            else:
                printf("%s "%(str(res)))
            printf("\n")


if __name__ == "__main__": 
    main()
    sys.exit(0)
