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


if PY3:
    def conv(s):
        return str.encode(s)
else:
    def conv(s):
        return s
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
    parser.add_argument('--outfile', type=str,help='actually infiles', nargs='+', required=True)
    parser.add_argument('--ignore', default=False,  action='store_true')
    parser.add_argument('--update', default=False,  action='store_true')
    parser.add_argument('--map',type=str, nargs='+',default=[])
    parser.add_argument('--csv-columns',type=str, nargs='+',default=None)



    args = parser.parse_args()
    for k in args.__dict__:
        printf("%s %s\n"%(k,str(args.__dict__[k])),e=True)
        printf("DB=%s\n"%(os.environ.get('DB')),e=True)


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

        max_id_in_pp = os.popen("sqlite3 %s 'select MAX(id) from pp'"%os.environ.get('DB')).read().strip()
        printf("max_id_in_pp = [%s]\n"%(max_id_in_pp),e=True)
        if max_id_in_pp == '':
            max_id_in_pp=-1
        else:
            max_id_in_pp=int(max_id_in_pp)
        start_id_in_pp=max_id_in_pp+1


        q_port = conv("""
.separator " "
drop table if exists {x};
drop index if exists {x}_i;
.import '{outfile}' {x}
select count(*) from {x};
CREATE UNIQUE INDEX {x}_i  ON {x} ("#id_Cluster");

.schema {x}
.quit
        """.format(outfile=outfile, x='tmp'))
        printf(q_port)
        subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stderr=sys.stderr, stdin=subprocess.PIPE ).communicate(q_port)
        vs=[]
        ks=[]
        for k in header:
            if args.csv_columns is not None and k not in args.csv_columns:
                continue
            if k not in cv:
                cv[k]=k
            vs.append(cv[k])
            ks.append(k)



        q_insert_raw = """

        insert {or_ignore} into pp(snap_id, id_cluster, {vs})    select {snap_id}, {x}."#id_cluster",{xks} from {x};
        """
        printf(q_insert_raw, e=True)
        print(vs)
        print(ks)
        if (len(vs)==0):
            continue
        q_insert = q_insert_raw.format(outfile=outfile, x='tmp',snap_id=snap.id, max_id_cluster=max_id_cluster, min_id_cluster = min_id_cluster, start_id_in_pp=start_id_in_pp,
                                       vs=','.join(vs), xks=','.join(['tmp.%s'%v for v in ks]),
                                       or_ignore= 'or ignore' if args.ignore else ''
        )
            
        printf(q_insert, e=True)
        child = subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stdin=subprocess.PIPE, stderr=sys.stderr)
        child.communicate(conv(q_insert))
        estatus = child.returncode
        if(estatus!=0):
            raise Exception("squilite exited with nonzero exit status %d"%(estatus))

        if args.update:
            for k in header:
                if args.csv_columns is not None and k not in args.csv_columns:
                    continue
                printf("csv key=%s -> %s\n"%(k,cv[k]))

                
                q_update = """
        update pp  set  {v} = (
            select cast({x}.{k} as float) from {x}
            where cast({x}."#id_cluster" as  int)=pp.id_cluster
        )
        where 
       snap_id={snap_id} and pp.id_cluster <= {max_id_cluster} and pp.id_cluster >= {min_id_cluster} and
       EXISTS (
            SELECT {x}."#id_cluster"
            FROM {x}
            where cast({x}."#id_cluster" as  int)=pp.id_cluster
        );

.quit
        """.format(outfile=outfile, x='tmp',k=k,v=cv[k],snap_id=snap.id, max_id_cluster=max_id_cluster, min_id_cluster = min_id_cluster, start_id_in_pp=start_id_in_pp)



                printf(q_update)
                child = subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stdin=subprocess.PIPE, stderr=sys.stderr)
                child.communicate(conv(q_update))
                estatus = child.returncode
                if(estatus!=0):
                    raise Exception("squilite exited with nonzero exit status %d"%(estatus))
        qdrop="""
drop index  {x}_i;
drop table {x};

.quit
""".format(outfile=outfile, x='tmp')
        print(qdrop)
        subprocess.Popen(('sqlite3',os.environ.get('DB')), stdout=sys.stdout, stderr=sys.stderr, stdin=subprocess.PIPE).communicate(conv(qdrop))


if __name__ == "__main__":
    main()

