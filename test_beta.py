import numpy as np
import g3read as g

""" EDIT THIS DATA: """
#simcut output:
filename = "Magneticum/Box2_hr/snap_060/22/simcut/7d2726p96wbrmms2/snap_060"

#compute everything within this radius:
cut_radius = 801.

#mu
mu=0.6

""" DONT EDIT ANYMORE """
f = g.GadgetFile(filename)

#
#the function returns a data structure for all selected blocks (POS, VEL, MASS, TEMP)
#and stack the data for the various particle types (0,1,2,3,4,5), where 0=gas, 1=dark matter, 4=stars, 5=black holes.
#For instance, you can access all positions readin data["POS "]
#If you need data separated per particle type, run
#data = f.read_new(blocks=[...], ptypes=[...], only_joined_ptypes=False)
#and you can access the properties for each data type, for instance gas particles, using data["POS "][0]
#
data = f.read_new(blocks=["POS ","VEL ","TEMP","MASS"], ptypes=[0,1,2,3,4,5])

center = np.average(data["POS "],weights=data["MASS"],axis=0)

#the function 'g.to_spherical()' returns data with columns 0,1,2 being rho,theta,phi
spherical_cut = g.to_spherical(data["POS "],center)[:,0]<cut_radius

vel = data["VEL "][spherical_cut]
T_inside_radius = data["TEMP"][spherical_cut]

#in the previous lines we loaded the block temperature for all particles, 
#but only gas particles have a temperature, so the library fills
#the particles
T_inside_radius = T_inside_radius[~np.isnan(T_inside_radius)]
radial_vel = g.to_spherical(data["VEL "],[0.,0.,0.])[:,0]

avg_vel = np.mean(radial_vel)
avg_vel2 =  np.mean(radial_vel**2)
sigma2_vel  = avg_vel2 - avg_vel*avg_vel
meanT = np.mean(T_inside_radius) 

print()
print("cut radius [kpc/h] = %.1f "%(cut_radius))
print("mass weighted center of mass [kpc/h] = %.1f %.1f %.1f "%(center[0], center[1], center[2]))
print("sigma velocity [km/s] =  %.1f "%(np.sqrt(sigma2_vel)))
print("mass weighted mean temperature [KeV] = %.2f "%(meanT/1.16e7))
print("beta = sigma**2/(KbT/mu*m_p) = %.2f "%((1e6*sigma2_vel)/(meanT*1.38e-23)*mu*1.66e-27))
print()

