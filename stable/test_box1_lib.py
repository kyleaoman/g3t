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
from_icluster = 0

""" BEGIN """

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
            output_path='tmp/cheese_%d'%(icluster)
            
        )

        printf(" - id: %d\n"% cluster_data.cluster_id)
        printf("   fof path: %s\n"%(groupbase))
        #printf("   position_in_fof_file: %d\n"%(icluster_file))
        #printf("   n satellites = %d\n"%(len(cluster_data.satellites()['SPOS'])))
        #print(cluster_data.satellites())
        printf("   mcri: %e\n"% cluster_data.mcri())
        printf("   rcri: %f\n"% cluster_data.rcri())
        #printf("   z: %.2e\n"% cluster_data.z())
        #printf(" fossilness = %s\n"% str(cluster_data.fossilness()))
        #printf(" virialness = %s\n"% str(cluster_data.virialness()))
        printf("   c200c_dm: %s\n"% str(cluster_data.c200c()))
        printf("   c200c_all: %s\n"% str(cluster_data.c200c(all_ptypes=True)))
        #         printf(" pictures = %s\n"%         cluster_data.pictures())
        #printf(" spinparameter = %s\n"%         cluster_data.spinparameter())

        printf("\n")
