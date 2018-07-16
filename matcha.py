import  matplotlib
matplotlib.use('Agg')
matplotlib.interactive(False)
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import sys
from multiprocessing import Process, Lock
import pp 
import g3read as g
import json
from collections import OrderedDict as odict
import multiprocessing
import time
import signal
import functools

def iw():
    signal.signal(signal.SIGINT, signal.SIG_IGN)



def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)


class O(object):
    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]
    def __str__(self):
        return str(self.__dict__)


def cached_pp(shared, **kw):
    _cache = shared._cache_pp
    if shared.pp_lock: shared.pp_lock.acquire()
    uid = json.dumps(sorted(kw.items()))
    if uid not in _cache:
        _cache[uid] = pp.PostProcessing(**kw)
    if shared.pp_lock: shared.pp_lock.release()
    return _cache[uid]

def main():


    folder='Box0mr_bao_dm'


    initial_snap='011'
    final_snap='037'
    id_cluster_end=10
    id_cluster_start=2
    group_base1='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao/groups_%s/sub_%s'
    group_base2='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_dm/groups_%s/sub_%s'
    snap_base1='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao/snapdir_%s/snap_%s'
    snap_base2='//smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_dm/snapdir_%s/snap_%s'
    """


    folder='Box2hr_bao_dm_2'
    initial_snap ='044'
    #confy['final_snap']='140'
    final_snap ='140'
    group_base1='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box2/hr_bao/groups_%s/sub_%s'
    snap_base1='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box2/hr_bao/snapdir_%s/snap_%s'

    group_base2='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box2/hr_dm/groups_%s/sub_%s'
    snap_base2='/smgpfs/work/pr83li/lu78qer5/Magneticum/Box2/hr_dm/snapdir_%s/snap_%s'

    """
    matcha(group_base1, snap_base1, group_base2, snap_base2, initial_snap, final_snap, folder=folder, parallel=True, n_processes=16, id_cluster_end=id_cluster_end, also_dm=True, id_cluster_start=id_cluster_start, skip_bao=True)


def find_object_in_other_snap(shared,  cluster_data,  groupbase, snapbase, nfiles=20, folder='.', outpath='', max_distance=2000., core_ids=None, check_ids=True, dm=False):
        icluster_match = -1
        for ifile_match  in range(0, nfiles):
            #fofpath_match = groupbase%(snap_match, snap_match)+'.'+str(ifile_match)
            fofpath_match = groupbase+'.'+str(ifile_match)
            #printf("              fof file match: %s\n"%(fofpath_match))
            s_match = pp.fof_info(fofpath_match, is_snap=False)
            nclusters_in_match_file = s_match.header.npart[0]
            for icluster_file_match in range(nclusters_in_match_file):
                icluster_match = icluster_match+1
                #printf("                      icluster_match: %s\n"%(fofpath_match))
                cluster_data_match = cached_pp(shared,
                                               cluster_id=icluster_match,
                                               cluster_id_in_file=icluster_file_match,
                                               cluster_i_file=ifile_match,
                                               group_base = groupbase, #e%(snap_match, snap_match),
                                               snap_base = snapbase, #%(snap_match, snap_match),
                                               n_files=nfiles,
                                               subfind_and_fof_same_file=False,
                                               dm=dm,
                                               output_path=outpath#+'_'+snap_match
                                               )

                distance = g.periodic_distance(cluster_data.gpos(), cluster_data_match.gpos(), cluster_data.box_size() )
                #printf("              distance(%d) = %f\n"% (cluster_data_match.cluster_id, distance))

                fraction=None
                #print(distance, fraction, cluster_data.can_read(),check_ids)
                if distance < max_distance:
                    if  check_ids and  cluster_data_match.can_read():
                        fraction = cluster_data.fraction_cluster_match(cluster_data_match,core_ids1=core_ids)
                        printf("              fraction(%d) = %f\n"%( cluster_data_match.cluster_id, fraction))

                #print(distance, fraction)
                
                if (fraction is None and distance < max_distance) or (fraction is not None and fraction>0.2):
                    
                    if cluster_data_match.can_read():
                        
                        printf("                  id = %d\n"% cluster_data_match.cluster_id)
                        printf("                  position in fof file = %d\n"%(cluster_data_match.cluster_i_file))
                        printf("                  mcri = %e\n"% cluster_data_match.mcri())
                        printf("                  rcri = %f\n"% cluster_data_match.rcri())
                        printf("                  z = %.2e\n"% cluster_data_match.z())
                        printf("                  RHMS central = %s\n"% str(cluster_data_match.rhms_central()))
                        printf("                  fossilness = %s\n"% str(cluster_data_match.fossilness()))
                        printf("                  c200c = %s\n"% str(cluster_data_match.c200c()))
                        #printf("                  spinparameter = %s\n"%         cluster_data_match.spinparameter().Lambda_all)
                        if check_ids:
                            printf("                  fraction = %.2f\n"%fraction)
                        printf("                  distance = %.2f\n"%distance)
                    else:
                        printf("                  id = %d\n"% cluster_data_match.cluster_id)
                        printf("                  position in fof file = %d\n"%(cluster_data_match.cluster_i_file))
                        printf("                  mcri = %e\n"% cluster_data_match.mcri())
                        printf("                  rcri = %f\n"% cluster_data_match.rcri())
                        printf("                  z = %.2e\n"% cluster_data_match.z())
                        printf("                  RHMS central = %s\n"% str(cluster_data_match.rhms_central()))
                        printf("                  fossilness = %s\n"% str(cluster_data_match.fossilness()))
                        printf("                  distance = %.2f\n"%distance)


                    return cluster_data_match




def follow_cluster(shared,  initial_snap, final_snap, icluster_file, icluster, ifile, groupbase,snapbase , nfiles=20, folder='.', outpath='', max_distance=2000., dm=False, n_files_after=20):
    initial_snap_int = int(initial_snap)
    final_snap_int = int(final_snap)

    cluster_data = cached_pp(shared,
                             cluster_id=icluster,
                             cluster_id_in_file=icluster_file,
                             cluster_i_file=ifile,
                             group_base = groupbase%(initial_snap, initial_snap),
                             snap_base = snapbase%(initial_snap, initial_snap),
                             n_files=nfiles,
                             subfind_and_fof_same_file=False,
                             output_path=outpath+'_'+initial_snap,
                             dm=dm
                             )

    printf("   id = %d\n"% cluster_data.cluster_id)
    printf("   position in fof file = %d\n"%(icluster_file))
    printf("   mcri = %e\n"% cluster_data.mcri())
    printf("   rcri = %f\n"% cluster_data.rcri())
    printf("   z = %.2e\n"% cluster_data.z())
    printf("   RHMS central = %s\n"% str(cluster_data.rhms_central()))
    printf("   fossilness = %s\n"% str(cluster_data.fossilness()))
    printf("   c200c = %s\n"% str(cluster_data.c200c()))
    #printf("   spinparameter = %s\n"%         cluster_data.spinparameter().Lambda_all)


    center = cluster_data.gpos()
    d = cluster_data.rcri()
    blocks="ID  "
    ptypes=1
    core_ids =cluster_data.core_ids()
    
    printf("   core ids size: %d\n"%(len(core_ids)))
    printf("\n")

    bucket=[cluster_data]

    for snap_int in range(initial_snap_int+1, final_snap_int+1):
        snap_match = "%03d"%(snap_int)
        printf("        snap match = %s\n"%(snap_match))
        cluster_data_match = find_object_in_other_snap(shared,
                                                       cluster_data,
                                                       groupbase%(snap_match,snap_match),
                                                       snapbase%(snap_match,snap_match),
                                                       nfiles=cluster_data.cluster_i_file+n_files_after,
                                                       folder=folder,
                                                       outpath=outpath+'_'+snap_match,
                                                       max_distance=max_distance,
                                                       core_ids=core_ids,
                                                       dm=dm)
        if cluster_data_match is not  None:
            if cluster_data_match.can_read():
                core_ids = cluster_data_match.core_ids()
                cluster_data_match.pictures_ptypes()
            bucket.append(cluster_data_match)
            cluster_data = cluster_data_match

    cluster_data = None
            
    for bro in bucket:
        if bro is None:
            continue

            

    properties=odict()
    properties["mcri"]=  [bro.mcri() for bro in bucket]
    properties["rcri"]=  [bro.rcri() for bro in bucket]
    properties["1./rs"]=  [bro.c200c().c/bro.rcri() if bro.can_read() else np.nan for bro in bucket]
    properties["c200c"]=  [bro.c200c().c if bro.can_read() else np.nan for bro in bucket]
    properties["M cent"]=  [bro.fossilness().first_mass for bro in bucket]
    properties["1./M sat"]= [1./bro.fossilness().most_massive_not_first for bro in bucket]
    properties["foss"]=  [bro.fossilness().fossilness for bro in bucket]
    properties["rhms cent"]= [ bro.rhms_central() for bro in bucket]
    #properties["spin"]= [bro.spinparameter().Lambda_all if bro.can_read() else np.nan  for bro in bucket]

    sfs = np.array([1./(1.+bro.z()) for bro in bucket])
    f, axarr = plt.subplots(len(properties), sharex=True, figsize=(12,30))
    fs=30
    iprop=-1
    for property_name in properties:
        iprop+=1
        
        ys = np.array(properties[property_name])

        maska = ~np.isnan(ys)
        #print (sfs)
        #print (ys)
        #print (maska)
        axarr[iprop].plot(sfs[maska],ys[maska], marker='x')

        axarr[iprop].set_ylabel(property_name,fontsize=fs)
        axarr[iprop].set_yscale("log")
        #axarr[iprop].set_xscale("log")


        for iline in range(len(ys)):
            if ys[iline]>0.:
                axarr[iprop].axvline(x=sfs[iline])
    axarr[len(properties)-1].set_xlim([0.,1.])
    axarr[len(properties)-1].set_xlabel('1/1+z', fontsize=fs)
    f.savefig(outpath+'line')

import traceback
import sys


def ciao(*l,**kw):
    try:
        l[0](*l[1:], **kw)
    except:
        traceback.print_exc(file=sys.stderr)    
        with open('st.log','a') as log:
            traceback.print_exc(file=log)
    
def apply_async(pool, f,*l,**kw):
    #print("running pool async!")
    pool.apply_async(ciao,(f,)+ l, kw)    

def matcha(group_base1, snap_base1, group_base2, snap_base2, initial_snap, final_snap,ifiles=10, id_cluster_start=0, id_cluster_end=20, folder='.', distance=2000., also_dm=True, skip_bao=False, parallel=True,n_processes=8, n_files_after=3):


    shared = pp.O()
    shared._cache_pp = {}
    shared.pp_lock =  None #Lock()



    initial_snap_int = int(initial_snap)
    final_snap_int = int(final_snap)
    if parallel:
        jobs=[]
        pool = multiprocessing.Pool(n_processes,iw)


    icluster = -1
    printf("matcha ifiles=%d .. %d\n"%(0,ifiles))
    for ifile  in range(0, ifiles):
        fofpath = group_base1%(initial_snap, initial_snap)+'.%d'%(ifile)
        printf("fof file: %s\n"%(fofpath))
        s = pp.fof_info(fofpath, is_snap=False)
        nclusters_in_file = s.header.npart[0]
        for icluster_file in range(nclusters_in_file):
            icluster = icluster+1
            if icluster<id_cluster_start:
                continue
            if icluster>id_cluster_end:
                break
            outpath = '%s/%s_cheese_%d_%s_'%(folder,'bao',icluster,initial_snap)
            if not skip_bao:
                if parallel:
                    apply_async(pool, follow_cluster, shared,  initial_snap, final_snap, icluster_file, icluster, ifile,
                           group_base1,
                           snap_base1, nfiles=ifile+ifiles,
                           outpath=outpath,
                           max_distance=distance)
                else:
                    follow_cluster(shared,  initial_snap, final_snap, icluster_file, icluster, ifile,  
                           group_base1, 
                           snap_base1, 
                           nfiles=ifile+ifiles, 
                           outpath=outpath,
                           max_distance=distance)

            if also_dm:
                cluster_data = cached_pp(shared,
                                         cluster_id=icluster,
                                         cluster_id_in_file=icluster_file,
                                         cluster_i_file=ifile,
                                         group_base = group_base1%(initial_snap, initial_snap),
                                         snap_base = snap_base1%(initial_snap, initial_snap),
                                         n_files=ifiles,
                                         subfind_and_fof_same_file=False,
                                         output_path=outpath
                             )
                cluster_data_dm= find_object_in_other_snap(shared,
                    cluster_data,
                    group_base2%(initial_snap, initial_snap),
                    snap_base2%(initial_snap, initial_snap),
                    nfiles=cluster_data.cluster_i_file+ifiles,
                    folder=folder,
                    outpath=outpath,
                    max_distance=distance,
                                                           check_ids=False,
                                                           dm=True)
                if cluster_data_dm is None:
                    continue
                if parallel:
                    apply_async(pool, follow_cluster, 
                                shared,  initial_snap, final_snap,
                                cluster_data_dm.cluster_id_in_file, 
                                cluster_data_dm.cluster_id,
                                cluster_data_dm.cluster_i_file,
                                group_base2, 
                                snap_base2,
                                nfiles=ifile+ifiles, 
                                       outpath='%s/%s_cheese_%d_%s_'%(folder,'dm',icluster,initial_snap),
                                       max_distance=distance,
                                dm=True
                                     )
                else:
                    follow_cluster(shared,  initial_snap, final_snap,
                               cluster_data_dm.cluster_id_in_file, 
                               cluster_data_dm.cluster_id,
                               cluster_data_dm.cluster_i_file,
                           group_base2, 
                           snap_base2, 
                           nfiles=ifile+ifiles, 
                           outpath='%s/%s_cheese_%d_%s_'%(folder,'dm',icluster,initial_snap),
                           max_distance=distance,
                               dm=True)

        else: #python magic, no idea
            continue
        break
    if parallel:
        print("closing..")
        pool.close()
        pool.join()
    print("return...")

if __name__=='__main__':
    main()
