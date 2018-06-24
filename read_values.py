import numpy as np
import g3read as g

""" EDIT THIS DATA: """
filename = "Magneticum/Box2_hr/snap_060/22/simcut/7d2726p96wbrmms2/snap_060"


xc = 288063.69
yc = 256522.44
zc = 347856.47

radius = 801.0

mu=0.6

""" DONT EDIT ANYMORE """
f = g.GadgetFile(filename)
kev_toKelvin = 11604525.00617
kev_toJoul = 1.66e-16

data = f.read_new(blocks=["POS ","MASS","VEL "], ptypes=[0,1,2,3,4,5])

center = np.array([xc,yc,zc])
relative_distance = np.abs(data["POS "]-center)
mask_inside_radius = (np.sqrt(relative_distance[:,0]**2.+ relative_distance[:,1]**2. + relative_distance[:,2])<radius)

vel_inside_radius = data["VEL "][mask_inside_radius]

radial_vel = np.sqrt(vel_inside_radius[:,0]**2. + vel_inside_radius[:,1]**2. + vel_inside_radius[:,2]**2.)

avg_vel = np.mean(vel_inside_radius)
avg_vel2 =  np.mean(vel_inside_radius*vel_inside_radius)
sigma2_vel  = avg_vel2 - avg_vel*avg_vel

gas_data = f.read_new(blocks=["POS ","TEMP","MASS"], ptypes=[0])
gas_relative_distance = np.abs(gas_data["POS "]-center)
mask_gas_inside_radius = (np.sqrt(gas_relative_distance[:,0]**2.+ gas_relative_distance[:,1]**2. + gas_relative_distance[:,2])<radius)


T_inside_radius = gas_data["TEMP"][mask_gas_inside_radius]
Mgas_inside_radius = gas_data["MASS"][mask_gas_inside_radius]

meanT = np.mean(T_inside_radius) #, weights=Mgas_inside_radius)

print "sigma2 [km/s]**2 %.3e "%(sigma2_vel)
print "sigma2 [m/s]**2 %.3e "%(1e6*sigma2_vel)
print "meanT [Kelvin]  %.3e "%(meanT)
print "meanT [KeV] %.2f "%(meanT/kev_toKelvin)
print "beta %.2f"% ((1e6*sigma2_vel)/(meanT*1.38e-23)*mu*1.66e-27)

