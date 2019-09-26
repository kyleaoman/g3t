#!/usr/bin/python
import sys
import g3read
import h5py

HDF5_MAP = {  'pos':'Coordinates',
              'vel':'Velocities',
              'id':'ParticleIDs',
              'mass':'Masses',
              'u':'InternalEnergy',
              'sfr':'StarFormationRate',
              'nh':'NeutralHydrogenAbundance',
              'metallicity':'Metallicity',
              'sigma':'Sigma',
              'tmax':'TemperatureMax',
              'delaytime':'DelayTime',
              'metalarray':'Metallicity',
              'rho':'Density',
              'hsml':'SmoothingLength',
              'ne':'ElectronAbundance',
              'age':'StellarFormationTime',
              'pot':'Potential',
              'fh2':'FractionH2',
              'nspawn':'NstarsSpawn',
              'abvc': 'ArtificialViscosity',
              'hott':'HotPhaseTemperature',
              'zs':'Mass of Metals',
              'temp':'Temperature',
              'vrms':'RMSVelocity',
              'phid':'DPotentialDt',
              'deti':'DelayTime',
              'vblk':'BulkVelocity',
              'tngb':'TrueNumberOfNeighbours',
              'cldx':'CloudFraction',
              'acrs':'StellarSpreadingLength',
              'hsms':'StellarSmoothingLength',
              'im': 'SSPInitialMass',
              'acrb':'BH_AccreationLength',
              'bhpc':'BH_NProgs',
              'bhma':'BH_Mass',
              'bhmd':'BH_Mdot'}

PY3 = sys.version_info[0] == 3

def printf(s,e=False,fd=None):
    if fd is None:
        fd=sys.stderr if e else sys.stdout
    fd.write(s)

def main(infile,outfile):


    f = g3read.GadgetFile(infile)
    with h5py.File(outfile, "w") as g:
        for ptype in [0,1,2,3,4,5]:
            if f.header.npart[ptype]==0: continue
            printf("ptype=%d\n"%(ptype))
            for block in f.blocks:
                if not f.blocks[block].ptypes[ptype]: continue
                lowerblock = block.lower().strip()
                if lowerblock in HDF5_MAP:
                    subgroup_name = "PartType%d/%s"%(ptype,HDF5_MAP[lowerblock])
                else:
                    raise Exception("I don't know the HDF5 name of block '%s'"%(block))
                printf("    block='%s' -> %s\n"%(block,subgroup_name))

                dset = g.create_dataset(subgroup_name, data = f.read(block,ptype))

if __name__ == "__main__":
    if len(sys.argv)!=3:
        printf(" \n",e=True)
        printf(" (Open)gadget2+3 to HDF5 format \n",e=True)
        printf(" by Antonio Ragagnin, 2018\n",e=True)
        printf(" \n",e=True)
        printf(" usage: python gadget_to_hdf5.py infile outfile\n",e=True)
        printf(" \n",e=True)
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])

