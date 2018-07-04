

#Table of Contents

  * [Reading gadget files and super indexes](#read-gadget)
    * [Reading single Gadget2/3 files](#read-gadget-single)
      * [Selecting multiple blocks at the same time](#select-multiple)
  * [Installation](#installation)
  * [Uninstallation](#uninstallation)
  * [Available plugins](#available-plugins)


# Reading gadget files and super indexes

You need to download the file `g3read.py`. It contains routines to read and write snapshots in single files (SimCut outpus) and to read large simulations that make use of super indexes (the IDL equivalent of `read_particle_in_a_box`)

## Reading single Gadget2/3 files

the function `read_new` can read 1 or multiple blocks for one or multiple particle types (0 is gas, 1 is dark matter, 4 is stars and 5 is black holes). To select particles from all particle types use a particletype = -1.

For instance, to select the positions and mass of all particles in a box:

```python
import g3read
f = g3read.GadgetFile("./test/snap_132")               
pos = f.read_new("POS", -1) #the -1 means to select all particles
x = pos[:,0]                             
y = pos[:,1]                             
mass =   f.read_new("MASS", -1)   

```
To select them for only gas particles do:

```python
pos_gas = f.read_new("POS", 0) #the 0 select only gas particles
x_gas = pos_gas[:,0]                             
y_gas = pos_gas[:,1]                             
mass_gas =  f.read_new("MASS", 0)  
````

### Selecting multiple blocks at the same time

If the first parameter of `read_new` is list of strings (instead of a string as in the previous examples), the function read_new will return a dictionary with each entry for each block

```python
data = f.read_new(["POS","MASS"], 0) #the -1 means 
x_gas = data["POS "][:,0]                             
y_gas = data["POS "][:,1]                             
mass_gas =  data["MASS"]
```

### Accessing blocks for different particle types

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


If you need to access also the blocks for single particle-type you can do it in two ways:

1) use the block `PTYPE` (Always added) in the following way:

```python
f = g3read.GadgetFile(filename)
data = f.read_new(blocks=["POS ","VEL ","TEMP","MASS"], ptypes=[0,1,2,3,4,5])

gas_temp = data["TEMP"][data["PTYPE"]==0] #zero is for gas,1 dm, 4 stars, 5 BH
```

Or you can ask read_new (or read_particles_in_box) to return a different array for each type, in the following way:


```python
f = g3read.GadgetFile(filename)
data = f.read_new(blocks=["POS ","VEL ","TEMP","MASS"], ptypes=[0,1,2,3,4,5], only_joined_ptypes=False)

gas_temp = data[0]["TEMP"]
dark_matter_masses = data[1]["MASS"]
all_types_masses= data[-1]["MASS"]
```


### Periodic boundary 

The `read_particles_in_a_box` will take care of adjusting the position of particles in a periodic box so that particles that have a distance from   `center` greater than half-box-size, 

You can call `read_new` with the keyword `center` and it will take care of the periodicity of the box:

```python
f = g3read.GadgetFile(filename)
positions = f.read_new(blocks=["POS ","VEL ","TEMP","MASS"], ptypes=[0,1,2,3,4,5], center=[25001., 54500., 12100.])

positions = data["POS "]
```



### Writing a block back to a (new) file

In this example I also use the pacakge `pp.py` that contains a routine to compute the gravitational potential between particles of the snapshot.

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

## Reading from a large simulation (reading simulations with superindexes)

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



# Submit a batch of jobs to the c2pap web portal (http://c2papcosmosim.uc.lrz.de/)

1) login to the portal

2) filter some clusters of interest and download the dataset in a csv file (e.g. `dataset.csv`)

3) download the file `c2pap_batch.py` rom this repository

4) execute it with `-s <Service name>` where the service name can be `SMAC`,`SimCut`,`PHOX`,`query`. 

6) set the csv file name with `-f daraset.csv`

5) append the service parameters after the `-p` parameter. Below the list of parameters:
```
                        Form parameters.
                            SimCut:
                            IMG_Z_SIZE
                            r500factor

                            SMAC:
                            content
                            IMG_SIZE
                            IMG_Z_SIZE
                            PROJECT
                            r500factor

                            PHOX:
                            mode
                            instrument (-1 for generic)
                            instrument_a (only if generic)
                            instrument_fov (only if generic)
                            t_obs_input
                            img_z_size
                            simulate

                            query:
                            query
                            page
                            limit
```
For instance the following will run a SMAC job over all objects in the dataset.csv:

```bash
python c2pap_batch.py -f dataset.csv -s SMAC -p content="bolometric x-ray luminosity" IMG_SIZE=512 IMG_Z_SIZE=5000 PROJECT='along z, xy plane' r500factor=2.0 -u <YOUR USERNAME> 
````

To avoid running duplicate jobs, use the flags ` --existing-jobs --cache-jobs cachefile.pickle` to make the script check for existing jobs with identical parameters


```


# Converting Gadget2/3 files to HDF5

Use the utility `gadget_to_hdf5.py`.

```bash
python gadget_to_hdf5.py infile outfile
```

In case you need to map names diffrently from the default version, have a look at the source code of `gadget_to_hdf5.py` and edit your own mapping.

```bash
python c2pap_batch.py -f dataset.csv -s SMAC -p content="bolometric x-ray luminosity" IMG_SIZE=512 IMG_Z_SIZE=5000 PROJECT='along z, xy plane' r500factor=2.0 -u <YOUR USERNAME> --existing-jobs --cache-jobs cachefile.pickle
````

