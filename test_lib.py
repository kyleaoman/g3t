import  matplotlib
matplotlib.interactive(False)
import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import sys


import pp 
import g3read as g


def heatmap(x,y,mass):
    heatmap, xedges, yedges = np.histogram2d(x, y, weights=mass, bins=50)
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
    f, ax = plt.subplots(1, 1)
    ax.imshow(heatmap.T, extent=extent, origin='lower')
    plt.show()
def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)


""" TEST READ A SNAPSHOT """
"""
f = g.GadgetFile("./test/snap_132")

data = f.read_new(blocks=["POS ","MASS"], ptypes=[0,1,2,3,4,5])

x = data["POS "][:,0]
y = data["POS "][:,1]
mass = data["MASS"]*1.e10

heatmap(x,y,mass)
"""

""" TEST READ MAGNETICUM SIMS """

"""
snapbase = '/HydroSims/Magneticum/Box2/hr_bao/snapdir_136/snap_136'
groupbase = '/HydroSims/Magneticum/Box2/hr_bao/groups_136/sub_136'


fof =  g.GadgetFile(groupbase+'.0', is_snap=False)
halo_positions = fof.read("GPOS",0)
halo_radii = fof.read("RVIR",0)

#extract position of first halo
first_halo_position = halo_positions[0]
first_halo_radius = halo_radii[0]

f = g.read_particles_in_box(snapbase,first_halo_position,first_halo_radius,["POS ","MASS"],[0,1,2,3,4,5])
x=f["POS "][:,0]
y=f["POS "][:,1]
mass =f["MASS"]
heatmap(x,y,mass)

"""

""" TEST READ MAGNETICUM SIMS """

properties = ['cluster_id','mcri','rcri','z','fossilness','c200c','virialness']
snapbase = '/HydroSims/Magneticum/Box2/hr_bao/snapdir_136/snap_136'
groupbase = '/HydroSims/Magneticum/Box2/hr_bao/groups_136/sub_136'

nfiles=10
icluster = -1
for ifile  in range(nfiles):
    s = g.GadgetFile(groupbase+'.'+str(ifile), is_snap=False)
    nclusters_in_file = s.header.npart[0]
    masses = s.read_new("MCRI",0)
    positions = s.read_new("RCRI",0)
    for icluster_file in range(nclusters_in_file):
        icluster = icluster+1
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

        printf(" id = %d\n"% cluster_data.cluster_id)
        printf(" fof path = %s\n"%(groupbase))
        printf(" position in fof file = %d\n"%(icluster_file))
        printf(" n satellites = %d\n"%(len(cluster_data.satellites()['SPOS'])))
        #print(cluster_data.satellites())
        printf(" mcri = %e\n"% cluster_data.mcri())
        printf(" rcri = %f\n"% cluster_data.rcri())
        printf(" z = %.2e\n"% cluster_data.z())
        printf(" fossilness = %s\n"% str(cluster_data.fossilness()))
        printf(" virialness = %s\n"% str(cluster_data.virialness()))
        printf(" c200c = %s\n"% str(cluster_data.c200c()))
        printf(" pictures = %s\n"%         cluster_data.pictures())

        printf("\n")
