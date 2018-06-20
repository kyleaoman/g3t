import matplotlib as mpl
mpl.use('Agg')
import numpy
import numpy as np
import pynbody
import argparse
from props import _props, _props_with_sats
from props import load_tables
from props import Structure
from props import FOF_TABLE_FILE_COL


def go(data):
    myfr=None
    myto=None
    cluster_range=None

    if "tag" in data["json"]: data["output"]=data["json"]["tag"]+data["output"]

    if data['one_of']!='':
        (one,of)=map(int, data['one_of'].split(','))
        nfiles=data['nclusters']
        one=one-1
        me=one
        ncpus=of
        init_fof_id=0
        print(init_fof_id,nfiles,ncpus,of,one)

        tot_elements=nfiles
        first_element=init_fof_id
        elements_per_cpu=1+nfiles//of
        n_domain=one


        min_fofid = init_fof_id +  elements_per_cpu*n_domain
        max_fofid = init_fof_id +  elements_per_cpu*(n_domain+1)
        if max_fofid>=tot_elements: max_fofid=tot_elements-1
        if min_fofid>=tot_elements: 
            print('TEMRINA min fof id =%d > tot_elements=%d'%(min_fofid,tot_elements))
            with open(data["output"],'w') as f:
                f.write('')
            return 
        ids=np.arange(max_fofid-min_fofid+1,dtype=np.int32)+min_fofid
        cluster_range=ids

    myfr=np.min(cluster_range)
    myto=np.max(cluster_range)
    print('CLUSTERS',ids)
    old_data=None

    if myfr is None and myto is None:
        task_share = tables = load_tables(data["fof"],data["sub"])
    else:
        task_share = tables = load_tables(data["fof"],data["sub"],skiplines=myfr,lines=myto-myfr,min_clusterid=myfr,max_clusterid=myto)

    fname=data["base"]+'/groups_'+data["snap"]+'/sub_'+data["snap"]
    #print(tables)
    fof_tables=tables["fof_table"]
    sf_tables=tables["sf_table"]
    nice_props='id z MsatMcd_Pratt MsatMcd_RatioRvir MsatMcdDM c200c  c500c mgas mvir mtot tgas mcri_noh mcri m5cc vr200'.split()


    if data["props"]=='*': data["props"]=','.join(nice_props)
    props = data["props"].split(',')
    add_props=[]
    mod_props=[]
    if data["edit"]!='':
        mod_props = data["edit"].split(',')
    if data["add"]!='':
        add_props = data["add"].split(',')

    all_props=props+add_props
    print(all_props)
    needs_sats=set(all_props).intersection(_props_with_sats)


    print('loading ',props)
    cols=[]
    prop_size=[]
    prop_pos=[]
    i_prop=0
    for propk in all_props:
        prop=_props[propk]
        prop_pos.append(i_prop)
        if 'l' in prop:
            for subcol in prop['l']:
                cols.append(subcol)
            prop_size.append(len(prop['l']))
            i_prop=i_prop+len(prop['l'])
    
        else:
            cols.append(propk)
            prop_size.append(1)
            i_prop=i_prop+1
        
    print('cols',cols,'prop_size',prop_size,'prop_pos',prop_pos)
    print(data, data["output"])
    m="w"
    if "m" in  data["json"]: m=data["json"]["m"]
    me=-1
    min_fof_id=myfr
    max_fof_id=len(fof_tables)+myfr
    if cluster_range is  None:
            cluster_range=range(min_fof_id,max_fof_id+1)
    if len(mod_props)>0:
        old_data=np.loadtxt(data["output"])
        
    open_flag='w'
    import os
    if not os.path.isfile(data["output"]):
        data['continue']=False

    if data['continue']:    open_flag='a'
    with open(data["output"],open_flag) as f:
        to_skip=0
        if not data['continue']:
            f.write("#"+" ".join(cols)+"\n")
            f.flush()
            line=-1
            print('BEEEEEEEEGIN',np.min(cluster_range),np.max(cluster_range),len(cluster_range),len(fof_tables),myfr)
        else:
            line=-1
            print('KONTINUEEEEEEEE',np.min(cluster_range),np.max(cluster_range),len(cluster_range),len(fof_tables),myfr)
            import commands
            sf_lines=int(commands.getstatusoutput("wc -l %s"%(data["output"]))[1].split()[0])-1
            print('KONTINUEEFROM',sf_lines,'lines')
            to_skip=sf_lines
        for fof_id in cluster_range:
            if to_skip>0:
                to_skip=to_skip-1
                print(data['rank'],'ABfofid=',fof_id,'skip')
                continue
            line=line+1


            if fof_id>=len(fof_tables)+myfr: break
            fof_object =Structure(fof_id,fname,
                                        fof_table=task_share["fof_table"],
                                        subfind_table=task_share["sf_table"],
                                        get_sats=needs_sats,  snap_file_name=data["base"]+'/snapdir_'+data["snap"]+'/snap_'+data["snap"],gl=data,myfr=myfr,mpirank=data['rank'], keyfiles=data['haskeys'],tag=data['s'])
            mvir = fof_object.get(data['mvir'])
            if 'mmass' in data  and mvir < data["mmass"]: 
                #print(data['rank'],'skiip',mvir,data['mmass'])
                continue
            #print(fof_object.get(data['mvir']))
            row=[]
            #map(lambda x: fof_object.get(x),props)
            prop_i=-1
            for prop in all_props:
                prop_i=prop_i+1
                if len(mod_props)>0 and prop not in mod_props and prop not in add_props:
                    res=old_data[line][prop_pos[prop_i]:prop_pos[prop_i]+prop_size[prop_i]].tolist()
                    #print('riciclo',prop,res)
                else:
                    if (data['rank']==1):
                        print(prop)
                    res= fof_object.get(prop)
                    if (data['rank']==1):
                        print(res)
                    #print('ricinputo',prop,res)
                #print(prop,res)
                if  isinstance(res, list) or isinstance(res,tuple):
                    for r in res:
                        row.append(r)
                else:
                    row.append(res)
            
            f.write(" ".join(map(str,row))+"\n")
            #print(" ".join(map(str,row)))
            print(data['rank'],'fofid=',fof_id,np.min(cluster_range),np.max(cluster_range)," ".join(map(str,row)))
            f.flush()
            
        print('EEEEEEEND')
    print('KLOSE')
def main():
    comm=None
    try:
        from mpi4py import MPI
        comm = MPI.COMM_WORLD
        rank = comm.Get_rank()+1
    except:
        import sys
        print "Unexpected error:", sys.exc_info()[0]
        print('NO MPI')

    import json
    d={"plot":True,"tag":"Result/"}
    print(_props.keys())
    import sys
    print(sys.argv)
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--base', type=str, help='base file name',default='../../m/Box0/mr_bao/groups_037/sub_037')
    parser.add_argument('--fof', type=str, default='fof.table')
    parser.add_argument('--sub', type=str, default='subfind.table')
    parser.add_argument('--s', type=str, default=None)
    parser.add_argument('--snap', type=str, default="037")
    parser.add_argument('--continue', type=json.loads, default='false')
    parser.add_argument('--output', type=str,help='output',default='my_table.table')
    parser.add_argument('--mmass', type=float,help='output',default=-1)
    parser.add_argument('--nclusters', type=int,help='output',default=0)
    parser.add_argument('--snap-base', type=str,help='output',default='snap_')
    parser.add_argument('--one-of', type=str,help='output',default='')
    parser.add_argument('--props', type=str,help='output',default='mvir,lgas')
    parser.add_argument('--edit', type=str,help='output',default='')
    parser.add_argument('--add', type=str,help='output',default='')
    parser.add_argument('--haskeys', type=json.loads,help='output',default=True)
    parser.add_argument('--mvir', type=str,help='output',default='mvir')
    parser.add_argument('--json', type=str,help='output',default=json.dumps(d)   )


    args = parser.parse_args()
    args.rank=rank
    args.one_of=args.one_of.replace('+',str(rank))
    print(args.json)
    d.update(json.loads(args.json))
    d['tag']=d['tag'].replace('+',str(rank))
    args.json=d
    print('go!',args.json)
    go(args.__dict__)


if __name__ == "__main__": main()

