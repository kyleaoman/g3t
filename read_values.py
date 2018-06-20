import numpy as np
import g3read as g

""" EDIT THIS DATA: """
filename = "./gwgogj5babb1xn3p/snap_136"

R_VIR = 2.*717.65
xc = 193731.56
yc = 163781.06
zc = 333743.56

radius = 1258.


""" DONT EDIT ANYMORE """
f = g.GadgetFile(filename)
kev_toKelvin = 11604525.00617
kev_toJoul = 1.66e-16

data = f.read_new(blocks=["POS ","MASS","VEL "], ptypes=[0,1,2,3,4,5])

center = np.array([xc,yc,zc])
relative_distance = np.abs(data["POS "]-center)
mask_inside_radius = (np.abs(relative_distance[:,0])<radius) & (np.abs(relative_distance[:,1])<radius) & (np.abs(relative_distance[:,2])<radius)

vel_inside_radius = data["VEL "][mask_inside_radius]

radial_vel = np.sqrt(vel_inside_radius[:,0]**2. + vel_inside_radius[:,1]**2. + vel_inside_radius[:,2]**2.)

avg_vel = np.mean(vel_inside_radius)
avg_vel2 =  np.mean(vel_inside_radius*vel_inside_radius)
sigma2_vel  = avg_vel2 - avg_vel*avg_vel

gas_data = f.read_new(blocks=["POS ","TEMP","MASS"], ptypes=[0])
gas_relative_distance = np.abs(gas_data["POS "]-center)
mask_gas_inside_radius = (np.abs(gas_relative_distance[:,0])<radius) & (np.abs(gas_relative_distance[:,1])<radius) & (np.abs(gas_relative_distance[:,2])<radius)


T_inside_radius = gas_data["TEMP"][mask_gas_inside_radius]
Mgas_inside_radius = gas_data["MASS"][mask_gas_inside_radius]

meanT = np.mean(T_inside_radius) #, weights=Mgas_inside_radius)

print "sigma2 [km/s]**2 = ",sigma2_vel
print "sigma2 [m/s]**2 = ",1e6*sigma2_vel
print "meanT [Kelvin] = ",meanT
print "meanT [KeV] = ",meanT/kev_toKelvin
print "beta", (1e6*sigma2_vel)/(meanT*1.38e-23)*.6*1.66e-27

