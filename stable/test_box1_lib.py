import  matplotlib
matplotlib.interactive(False)
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import sys


import pp 
import g3read as g


def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)


""" TEST READ MAGNETICUM SIMS """

snapbase = '/HydroSims/Magneticum/Box1a/mr_bao/snapdir_144/snap_144'
groupbase = '/HydroSims/Magneticum/Box1a/mr_bao/groups_144/sub_144'
from_icluster = 0 #id of first cluster to analyse
to_icluster = 11494 #id of last cluster to analyse

""" BEGIN """

printf("#cluster_id mcri[Msun] rcri[kpc] c200c_dm c200c_all\n")

nfiles=100
icluster = -1
for ifile  in range(nfiles):
    s = g.GadgetFile(groupbase+'.'+str(ifile), is_snap=False)
    nclusters_in_file = s.header.npart[0]
    masses = s.read_new("MCRI",0)
    positions = s.read_new("RCRI",0)
    for icluster_file in range(nclusters_in_file):
        icluster = icluster+1
        if icluster<from_icluster: continue
        cluster_data = pp.PostProcessing(
            cluster_id=icluster,
            cluster_id_in_file=icluster_file,
            cluster_i_file=ifile,
            group_base = groupbase,
            snap_base = snapbase,
            n_files=nfiles,
            subfind_and_fof_same_file=False,
            
        )
        cluster_id = cluster_data.cluster_id
        mcri = cluster_data.mcri()*1e10/.72
        rcri = cluster_data.rcri()/.72
        c200c_dm = cluster_data.c200c().c
        c200c_all = cluster_data.c200c(all_ptypes=True).c
        printf("%d %.3e %.3f %.3f %.3f \n"%(cluster_id, mcri, rcri, c200c_dm, c200c_all))
