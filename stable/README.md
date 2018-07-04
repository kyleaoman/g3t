# Reading single snapshots


```python
import g3read
f = g3read.GadgetFile("./test/snap_132")               
data = f.read_new(blocks=["POS ","MASS"], ptypes=[0,1,2,3,4,5])
x = data["POS "][:,0]                             
y = data["POS "][:,1]                             
mass = data["MASS"]*1.e10
```

# Overwriting a block in a single snapshot

```python
import g3read
import pp #used only to compute the gravitational potential
my_filename = "./test/snap_132"
my_filename_output "./test/new_snap_132"
f = g3read.GadgetFile(my_filename)

positions = f.read_new("POS ",-1) #-1 means all particles
masses = f.read_new("MASS",-1)
potential = pp.gravitational_potential(masses, positions, center).potential

f.write_block("POT ", -1, potential, filename=my_filename_output)

print("done.")

```

# Reading from a large simulation (reading simulations with superindexes)

```python
import g3read
snapbase = '/HydroSims/Magneticum/Box2/hr_bao/snapdir_136/snap_136'
groupbase = '/HydroSims/Magneticum/Box2/hr_bao/groups_136/sub_136'
fof =  g.GadgetFile(groupbase+'.0', is_snap=False) #if you read a FoF/Subfind file, add is_snap = False 

halo_positions = fof.read("GPOS",0) #block zero has FoF data, block 1 has SubFind data
halo_radii = fof.read("RVIR",0)

#extract position of first halo
first_halo_position = halo_positions[0]
first_halo_radius = halo_radii[0]

f = g3read.read_particles_in_box(snapbase,first_halo_position,first_halo_radius,["POS ","MASS"],[0,1,2,3,4,5])
x=f["POS "][:,0]
y=f["POS "][:,1]
mass =f["MASS"]
```

# Accessing blocks for different particle types

In case a you try to read a block for a particle type that does not have such a block, the values for that particle type will be NaN. 
This is very useful when you want to access blocks for both darkmatter and gas particles in one single function calls.

The following code computes the beta value for a cluster:

```python
import numpy as np
import g3read as g3read

filename = "snap_060"
cut_radius = 801. #consider only particles within this cut

f = g3read.GadgetFile(filename)
data = f.read_new(blocks=["POS ","VEL ","TEMP","MASS"], ptypes=[0,1,2,3,4,5]) #dark matter and star particles will have TEMP=NaN
center = np.average(data["POS "],weights=data["MASS"],axis=0)

#the function 'g.to_spherical()' returns data with columns 0,1,2 being rho,theta,phi
spherical_cut = g.to_spherical(data["POS "],center)[:,0]<cut_radius
vel = data["VEL "][spherical_cut]
T_inside_radius_wnans = data["TEMP"][spherical_cut]
T_inside_radius = T_inside_radius_wnans[~np.isnan(T_inside_radius_wnans)] #remove all NaNs
radial_vel = g.to_spherical(data["VEL "],[0.,0.,0.])[:,0]

sigma_vel  = np.sqrt(np.mean(radial_vel**2) - np.mean(radial_vel)**2.)
meanT = np.mean(T_inside_radius) 

print("sigma velocity [km/s] =  %.1f "%(np.sqrt(sigma_vel)))
print("mass weighted mean temperature [KeV] = %.2f "%(meanT/1.16e7))

```


# Converting Gadget2/3 files to HDF5

Use the utility `gadget_to_hdf5.py`.

```bash
python gadget_to_hdf5.py infile outfile
```

In case you need to map names diffrently from the default version, have a look at the source code of `gadget_to_hdf5.py` and edit your own mapping.
