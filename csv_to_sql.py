#!/usr/bin/python
import sys
from pp_schema  import *
import numpy as np
import numpy as np
import argparse
import os
import subprocess
from collections import OrderedDict as odict

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


    cv=odict()
    for mappa in args.map:
        chiave,valore = mappa.split('=')
        cv[chiave]=valore

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

    for outfile in args.outfile:
        with open(outfile,'r') as f:
            line = f.readline()
            header=line.split()[1:]

        min_id_cluster = os.popen("grep -v '#' %s | sort -n  | head -n1 | awk '{print $1}'"%outfile).read()
        max_id_cluster = os.popen("grep -v '#' %s |sort -rn  | head -n1 | awk '{print $1}'"%outfile).read()
        print("grep -v '#' %s | sort -n  | head -n1 | awk '{print $1}'"%outfile)
        printf("File=%s, Fields: %s\n"%(outfile,','.join(header)))

        subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stdin=subprocess.PIPE).communicate("""
.separator " "
drop table if exists {x};
.import '{outfile}' {x}
select count(*) from {x};
        CREATE INDEX {x}_i  ON {x} (id_cluster);
        CREATE INDEX {x}_i  ON {x} (id_cluster);

.schema {x}
.quit
""".format(outfile=outfile, x='tmp'))

        for k in header:
            printf("csv key=%s (%s)\n"%(k, cv[k]))

            q = """
        update fof 
        set  {v} = (
            select cast({x}.{k} as float) from {x}
            where cast({x}."#id_cluster" as  int)=fof.id_cluster
        )

 where 
snap_id={snap_id} and fof.id_cluster < {max_id_cluster} and fof.id_cluster > {min_id_cluster} and
EXISTS (
            SELECT {x}."#id_cluster"
            FROM {x}
            where cast({x}."#id_cluster" as  int)=fof.id_cluster
        ) 
;

.quit
        """.format(outfile=outfile, x='tmp',k=k,v=cv[k],snap_id=snap.id, max_id_cluster=max_id_cluster, min_id_cluster = min_id_cluster)
            printf(q)
            subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stdin=subprocess.PIPE).communicate(q)

        subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stdin=subprocess.PIPE).communicate("""
drop table if exists {x};
.quit
""".format(outfile=outfile, x='tmp'))


if __name__ == "__main__":
    main()

