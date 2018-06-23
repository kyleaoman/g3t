import g3read as g
#g.debug=True
import sys
import numpy as np
import math
import json
import scipy
import scipy.optimize
from six import with_metaclass



class O(object):
    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]
    def __str__(self):
        return str(self.__dict__)
profilo_nfw=lambda r,rho0,rs: rho0*1e-24 / ( (r/rs) * ((1.+r/rs)**2.))
def printf(s,e=False):
    fd=sys.stderr if e else sys.stdout
    fd.write(s)


def nfw_fit(mass,pos,center,R,hbpar=0.72, plot=None, oldRFactor=1.):
    m=mass
    p=pos
    delta=pos-center
    d=np.sqrt(delta[:,0]**2+delta[:,1]**2+delta[:,2]**2)

    oldR=R
    R=oldRFactor*R
    maskd=d<R
    m=m[maskd]
    p=p[maskd]
    d=d[maskd]
    nbins=150
    ii=np.argsort(d)
    the_num=42*math.pi #rlly?
    anz=len(d)
    nn=int(round(anz)/min([math.sqrt(anz),the_num]))
    part_anz=int(float(anz)/nn)
    numrb=round(20.*(part_anz/the_num)**.5)
    rmin=d[ii[part_anz]]
    dr=(np.log10(R)-np.log10(rmin))/(numrb-1)
    r_in_log=np.log10(rmin)+np.arange(numrb)*dr
    nn=int(numrb)
    kparsck= 3.085678e21
    solmas = 1.989e33
    rftab=np.zeros(nn)
    rhoftab=np.zeros(nn)
    rs1=np.zeros(nn)
    rs2=np.zeros(nn)
    nftab=np.zeros(nn)
    for ir in range(0,nn):
        if ir == 0:
            Vol1=0.0
            r1=0.0
        else:
            r1=10**r_in_log[ir-1]
            Vol1=(r1**3.)*4.0/3.0*math.pi*(kparsck**3.)*(hbpar**-3.)
         
        r2=10.**r_in_log[ir]
        Vol2=(r2**3.)*4.0/3.0*math.pi*(kparsck**3.)*(hbpar**-3.)
        jj=(d >= r1) & (d < r2)
        rs1[ir]=r1
        rs2[ir]=r2
        anz=len(d[jj])
        rftab[ir]=np.sum(d[jj])/anz/R
        rhoftab[ir]=np.sum(m[jj])*solmas/hbpar/(Vol2-Vol1)
        nftab[ir]=anz

    R=oldR
    if plot is not None:
        import matplotlib.pyplot as plt
        figo, axo = plt.subplots()
        axo.set_xscale("log")
        axo.set_yscale("log")
        axo.axvline(R)
        axo.set_xlabel("r [kpc]")
        axo.set_ylabel("Mass/vol [g*cm^-3]")
        #axo.axis("equal")
        axo.plot(rftab*R, rhoftab, label="Magneticum/Box2/z=0 cluster")
        axo.legend()
        figo.savefig(plot)
        #import sys
        sys.exit()

    r=rftab
    rho=rhoftab
    rho=rho*1e10
    minimize_me = lambda x: np.sqrt(

        np.sum(
            np.abs(
                np.log10(profilo_nfw(r,x[0],x[1])/rho)
                )**2
            ))


    x0=[0.05,0.5]
    method='L-BFGS-B'
    xbnd=[[0.001,50.0],[0.01,10.0]]
    res=scipy.optimize.minimize(minimize_me,x0,method=method,bounds=   xbnd)
    return res



def fossilness(masses, dists):
    try:




        sorted_ids_d=np.arange(len(masses))[np.argsort(dists)]
        first_mass=masses[sorted_ids_d[0]]
        other_ids=sorted_ids_d[1:]
        others_masses=masses[other_ids]
        most_massive_not_first=np.max(others_masses)
        return O(first_mass=first_mass, most_massive_not_first=most_massive_not_first,fossilness=first_mass/most_massive_not_first)
    except: #WHAT COULD POSSIBLY GO WRONG
        return  O(first_mass=np.nan, most_massive_not_first=np.nan,fossilness=np.nan)

def resize_order_and_sort(my_data, gpos, radius,cut=None):

    if cut is None:
        cut=radius
    for pt in my_data.keys():
        poses=my_data[pt]['POS ']
        if (len(poses))>0:
            delta=poses-gpos
            dists=np.sqrt(delta[:,0]**2+delta[:,1]**2+delta[:,2]**2)
            sid_dists=np.argsort(dists)
            mask_dist=sid_dists[dists[sid_dists]<cut]
            for k in my_data[pt].keys():
                my_data[pt][k]= my_data[pt][k][mask_dist]
            my_data[pt]['DIST']=dists[mask_dist]
        else:
            my_data[pt]['DIST']=[]
    return my_data


def add_dist(my_data, gpos):

    for pt in my_data.keys():
        poses=my_data[pt]['POS ']
        if (len(poses))>0:
            delta=poses-gpos
            dists=np.sqrt(delta[:,0]**2+delta[:,1]**2+delta[:,2]**2)
            my_data[pt]['DIST']=dists
        else:
            my_data[pt]['DIST']=[]
    return my_data

def fix_v(data,gpos,d=60.,H0=0.1):
    #H0=0.1

    #average_v=np.average(data[-1]['VEL '][data[-1]['DIST']<d],axis=0,weights=100000.*data[-1]['MASS'][data[-1]['DIST']<d])
    average_v=np.average(data[-1]['VEL '][data[-1]['DIST']<d],axis=0)

    for pt in data.keys():
        poses = data[pt]['POS ']
        if len(poses)>0:
            delta = (poses-gpos)
            data[pt]['VEL '] = (data[pt]['VEL ']-average_v)
            data[pt]['VEL '] -= delta*H0






def to_spherical(xyzt,center,ptype='bo'):
    #takes list xyz (single coord)
    import math
    xyz = xyzt.T
    x       = xyz[0]-center[0]
    y       = xyz[1]-center[1]
    z       = xyz[2]-center[2]
    r       =  np.sqrt(x*x+y*y+z*z)
    #supress warnings for z=0,r=0 and z/r=0/0
    r[r==0.]=-1.
    theta   =  np.arccos(z/r)
    r[r==-1.]=0.
    import sys
    phi     =  np.arctan2(y,x)
    phi[r==0.]=0.
    theta[r==0.]=0.
    return np.array([r,theta,phi]).T

def to_cartesian(rthetaphi):

    r       = rthetaphi[0]
    theta   = rthetaphi[1]
    phi     = rthetaphi[2]
    x = r * np.sin( theta ) * np.cos( phi )
    y = r * np.sin( theta ) * np.sin( phi )
    z = r * np.cos( theta )
    return [x,y,z]




def virialness(center, rcri, all_mass, all_pos, all_vel, all_potential, gas_mass, gas_pos, gas_vel, gas_u, gas_temp, H0=0.1, G=47003.1, cut=None, velcut=20.):

    gas =False  if (gas_mass is None or gas_vel is None or gas_pos is None) else True

    all_data={}
    all_data[-1]={}
    all_data[-1]["MASS"] = all_mass
    all_data[-1]["POS "] = all_pos
    all_sferical = to_spherical(all_pos, center)
    all_data[-1]["SPOS"] = all_sferical
    all_data[-1]["VEL "] = all_vel
    all_data[-1]["POT "] = all_potential
    if gas:
        all_data[0]={}
        all_data[0]["MASS"] = gas_mass
        all_data[0]["POS "] = gas_pos
        all_data[0]["VEL "] = gas_vel
        all_data[0]["TEMP"] = gas_temp
        all_data[0]["U   "] = gas_u

    if cut is None:
        cut = rcri
    resize_order_and_sort(all_data,center,rcri,cut=cut)
    fix_v(all_data,center,H0=H0,d=velcut)

    spherical_potential = all_potential
    W=np.sum( all_data[-1]['POT '] * all_data[-1]['MASS']*0.5)

    """ KINETIK """
    Vsq=np.sum(all_data[-1]['VEL ']*all_data[-1]['VEL '],axis=1)
    Kcoll=(np.sum(Vsq*all_data[-1]['MASS'])*0.5)
    if gas:
        Kgas = np.sum(all_data[0]['U   ']*all_data[0]['MASS'])
    else:
        Kgas=0.
    K=Kcoll+Kgas

    """ ES """
    Nall = all_data[0]["MASS"].shape[0]
    id_80bin=int(Nall*0.8)
    R_80bin=all_data[-1]['DIST'][id_80bin]
    R_mask = all_data[-1]['DIST']>R_80bin
    R_90bin= np.median(all_data[-1]['DIST'][R_mask])
    #Escoll=  np.sum((all_data[-1]['MASS']*Vsq*)[ids_more_than_R80])  #(R_90bin**3./(rcri**3.-R_80bin**3.))*( np.sum(all_data[-1]['MASS'][all_data[-1]['DIST']>R_80bin]*Vsq[all_data[-1]['DIST']>R_80bin]) )
    Escoll=  (R_90bin**3./(cut**3.-R_80bin**3.))*( np.sum(all_data[-1]['MASS'][all_data[-1]['DIST']>R_80bin]*Vsq[all_data[-1]['DIST']>R_80bin]) )



    K_bolzman_cgs=1.380e-16
    Gadget_energy_cgs = 1.989e53
    proton_mass_cgs=1.672e-24
    mu_wg_cui=0.588
    UnitMass_in_g = 1.989e+43
    if gas:
        all_data[0]['PsTerm'] = 3. * all_data[0]['TEMP'] * all_data[0]['MASS'] * UnitMass_in_g  * K_bolzman_cgs / (mu_wg_cui * proton_mass_cgs) / Gadget_energy_cgs

    if gas:
        Ngas=len(all_data[0]['MASS'])
        id_80bingas=int(Ngas*0.8)
        R_80bingas=all_data[0]['DIST'][id_80bingas]
        R_90bingas=np.median(all_data[0]['DIST'][all_data[0]['DIST']>R_80bingas])
        Esgas= (R_90bingas**3./(cut**3.-R_80bingas**3.))*np.sum(all_data[0]['PsTerm'][all_data[0]['DIST']>R_80bingas])
    else:
        Esgas=0.

    Es=Escoll+Esgas

    """ FINE """

    mu = -(2.*K-Es)/W

    return O(W=W,K=K,Es=Es, eta=-(2.*K-Es)/W, beta=-2.*K/W)




def gravitational_potential(masses, positions, gpos,
                            cut=None,
                            cut_type=None,
                            superkeys=True, G=47003.1,
                            set_to_value_after_cut=None,
                            spher_nbs=40, spher_nfi=4, spher_nteta=4, has_keys=True):

    all_data={}
    all_data[-1]={}
    all_data[-1]["MASS"]=masses
    all_data[-1]["POS "]=positions

    all_sferical = to_spherical(all_data[-1]["POS "], gpos)

    all_data[-1]["SPOS"] = all_sferical
    add_dist(all_data, gpos)


    Nall=len(all_data[-1]['MASS'])


    import math
    twopi=2.*math.pi
    pi=math.pi
    """    POTENTIAL    """
    spher_bs = [np.logspace(np.log10(np.min(all_data[-1]['SPOS'][:,0])+0.01),np.log10(np.max(all_data[-1]['SPOS'][:,0])),spher_nbs),np.linspace(0.,pi,spher_nteta), np.linspace(-pi,pi,spher_nfi)]


    mass_weights = all_data[-1]['MASS']
    if cut is not None and cut_type is not None:
        if cut_type=="sphere":
            mass_weights[all_data[-1]['DIST']>cut]=0.
        elif cut_type=="cube":
            mass_weights[np.abs(all_data[-1]['POS '][:,0]-gpos[0])>cut]=0.
            mass_weights[np.abs(all_data[-1]['POS '][:,1]-gpos[1])>cut]=0.
            mass_weights[np.abs(all_data[-1]['POS '][:,2]-gpos[2])>cut]=0.


    spher_all_ms, spher_b = np.histogramdd(all_data[-1]['SPOS'], weights=mass_weights, bins=spher_bs)

    spher_all_ds, spher_b = np.histogramdd(all_data[-1]['SPOS'], weights=all_data[-1]['SPOS'].T[0], bins=spher_bs)
    spher_all_ts, spher_b = np.histogramdd(all_data[-1]['SPOS'], weights=all_data[-1]['SPOS'].T[1], bins=spher_bs)
    spher_all_fs, spher_b = np.histogramdd(all_data[-1]['SPOS'], weights=all_data[-1]['SPOS'].T[2], bins=spher_bs)
    spher_all_ns, spher_b = np.histogramdd(all_data[-1]['SPOS'],  bins=spher_bs)


    spher_all_ns[spher_all_ns==0]=np.nan
    spher_all_cds = spher_all_ds/spher_all_ns
    spher_all_cts = spher_all_ts/spher_all_ns
    spher_all_cfs = spher_all_fs/spher_all_ns



    spher_all_x ,    spher_all_y ,    spher_all_z = to_cartesian([spher_all_cds,spher_all_cts,spher_all_cfs])

    shape=spher_all_ds.shape
    spher_b_delta_r=(spher_b[0][1:]-spher_b[0][:-1])
    spher_b_delta_t=(spher_b[1][1:]-spher_b[1][:-1])
    spher_b_delta_f=(spher_b[2][1:]-spher_b[2][:-1])

    shper_delta_rs = np.transpose( (np.transpose(np.ones(shape),axes=(2,1,0) )* (spher_b_delta_r)), axes=(2,1,0))
    shper_delta_ts = np.transpose( (np.transpose(np.ones(shape),axes=(0,2,1) )* (spher_b_delta_t)), axes=(0,2,1))
    shper_delta_fs = np.transpose( (np.transpose(np.ones(shape),axes=(0,1,2) )* (spher_b_delta_f)), axes=(0,1,2))

    spher_all_vols = spher_all_cds**2.*np.sin(spher_all_cts)*shper_delta_rs*shper_delta_ts*shper_delta_fs
    spher_all_rhos = spher_all_ms/spher_all_vols
    spher_all_ms = np.nan_to_num(spher_all_ms)
    def generate_fi(spher_b,spher_all_cds,spher_all_cts,spher_all_cfs,spher_all_x,spher_all_y,spher_all_z,spher_all_ms):
        fi=np.ones(spher_all_ds.shape)
        for bin_r in range(len(spher_b[0])-1):
            for bin_t in range(len(spher_b[1])-1):
                for bin_phi in range(len(spher_b[2])-1):
                    position_xyz = to_cartesian(np.array([spher_all_cds[bin_r,bin_t,bin_phi], spher_all_cts[bin_r,bin_t,bin_phi],spher_all_cfs[bin_r,bin_t,bin_phi]]))
                    distances = np.sqrt( (spher_all_x-position_xyz[0])**2. + (spher_all_y-position_xyz[1])**2. + (spher_all_z-position_xyz[2])**2.)
                    distances = np.nan_to_num(distances)
                    non_zero_distances = distances>0.
                    fi[bin_r,bin_t,bin_phi] = -G*np.sum(spher_all_ms[non_zero_distances]/distances[non_zero_distances])
        return np.nan_to_num(fi)
    fi =  generate_fi(spher_b,spher_all_cds,spher_all_cts,spher_all_cfs,spher_all_x,spher_all_y,spher_all_z,spher_all_ms)


    bin_all_h_i = np.digitize(all_data[-1]['SPOS'][:,0],spher_bs[0])-1
    bin_all_h_j = np.digitize(all_data[-1]['SPOS'][:,1],spher_bs[1])-1
    bin_all_h_k = np.digitize(all_data[-1]['SPOS'][:,2],spher_bs[2])-1

    bin_all_h_i[ bin_all_h_i>=len(spher_bs[0])-1 ]=len(spher_bs[0])-2 #bug of np, if a value is exactly a boundary, the bin is larger than it should
    bin_all_h_j[ bin_all_h_j>=len(spher_bs[1])-1 ]=len(spher_bs[1])-2
    bin_all_h_k[ bin_all_h_k>=len(spher_bs[2])-1 ]=len(spher_bs[2])-2

    bin_all_h=np.array([bin_all_h_i,bin_all_h_j,bin_all_h_k]).T
    bin_all_h_tuple = tuple( bin_all_h)


    somma_all_inte = fi[tuple ( bin_all_h.T)]

    """ set to zero things outside rcri"""
    if set_to_value_after_cut:
        somma_all_inte[all_data[-1]['SPOS'][:,0]>cut] = set_to_value_after_cut


    all_data[-1]["SPHERICAL_POTE"] = somma_all_inte
    return O(potential = all_data[-1]["SPHERICAL_POTE"])


def J_adelheid(basepath, gpos, rcri,  dm=False,   keys=True,G=47003.1):
    import np
    if dm:
        keys=False
    cut=rcri
    all_keys=['MASS','VEL ','POS ']
    all_pt=[0,1,2,3,4]
    all_data=g3.read_particles_in_box(basepath,gpos,cut,all_keys ,all_pt,has_super_index=keys)

    import math

    all_data[-1]={}
    new_pt=[]
    for i in all_pt:
        if len(all_data[i]['MASS'])==0:
            del all_data[i]
        else:
            new_pt.append(i)
    all_pt=new_pt
    proprio_all_pt=all_pt+[-1]
    for i in all_pt:
        all_data[i]['MOME'] = all_data[i]['VEL ']
        all_data[i]['MOME'][:,0] = all_data[i]['MOME'][:,0] * all_data[i]['MASS']
        all_data[i]['MOME'][:,1] = all_data[i]['MOME'][:,1] * all_data[i]['MASS']
        all_data[i]['MOME'][:,2] = all_data[i]['MOME'][:,2] * all_data[i]['MASS']


        all_data[i]['CPOS']= all_data[i]['POS ']-np.array(gpos)
    all_keys.append("MOME")
    all_keys.append("CPOS")
    for key in all_keys:
        all_data[-1][key]=np.concatenate(tuple([all_data[i][key] for i in all_pt]));
    resize_order_and_sort(all_data,gpos,rcri,cut=cut)


    res={}
    for i in [0,1,4,-1]:
        res[i]={}
        if i in  proprio_all_pt:
            J_vector = np.cross( all_data[i]['CPOS'], all_data[i]['MOME'] )
            J_sum = np.sum(J_vector,axis=0)
            J_modi = np.sqrt(J_sum[0]**2.+J_sum[1]**2. + J_sum[2]**2. )
            Mtot = np.sum(all_data[-1]['MASS'])
            Mtypein = np.sum(all_data[i]['MASS'])
            Lambda = J_modi*(Mtot**-1.5)*((2.*rcri)**-0.5)*(G**-0.5)
            #print("Lambda", i, Lambda, J_modi, Mtot,rcri,G, )
            res[i]["L"] = Lambda
            res[i]["Jspec"] = J_modi/Mtypein


            mask_in =  all_data[i]['DIST']<(0.3*rcri)
            r_in=0.3*rcri
            J_vector_in = np.cross(all_data[i]['CPOS'][mask_in], all_data[i]['MOME'][mask_in])
            J_sum_in = np.sum(J_vector_in,axis=0)
            J_modi_in = np.sqrt(J_sum_in[0]**2.+J_sum_in[1]**2. + J_sum_in[2]**2. )
            Mtot_in = np.sum(all_data[-1]['MASS'][mask_in])
            Mtypein = np.sum(all_data[i]['MASS'][mask_in])
            Lambda_in = J_modi_in*(Mtot_in**-1.5)*((2.*r_in)**-0.5)*(G**-0.5)
            res[i]["Lin"] = Lambda_in

            res[i]["Jspecin"] = J_modi_in/Mtypein


        else:
            res[i]["L"] = -1
            res[i]["Lin"] = -1
            res[i]["Jspec"] = -1
            res[i]["Jspecin"] = -1




    return res



def myDecorator(func):
    " Used on methods to convert them to methods that replace themselves\
        with their return value once they are called. "

    _cache = {}
    def cache(*a,**b):
        self = a # Reference to the class who owns the method
        
        if self not in _cache:
            _cache[self]={}
        cached = _cache[self]
        key = json.dumps({ "b":b})
        if key not in cached:
            cached[key] = func(*a,**b)
            #print ("returning ",func.__name__,a[0], a[1:], b)
        return cached[key]

    return cache

class myMetaClass(type):
    def __new__(cls, name, bases, local):
        #print("new meta")
        for attr in local:
            if attr[0]=='_' or not callable(local[attr]):
                continue
            #print("meta", attr)
            value = local[attr]
            if callable(value):
                local[attr] = myDecorator(value)
        return type.__new__(cls, name, bases, local)

class Queue(object):
    def __init__(self,size):
        self.items = []
        self.size=size
    def keys(self):
        return [item[0] for  item in self.items]
    def __contains__(self, key):
        return key in self.keys()
    def __getitem__(self, key):
        if key not in self.keys():
            raise Exception("No cached item with key '%s'"%(key))
        i=-1
        for _key in self.keys():
            i=i+1
            if key==_key:
                return self.items[i][1]
        raise Exception("No cached item with key '%s'"%(key))
    def __setitem__(self, key, value):
        if key in self:
            del self[key]
        self.items.insert(0,(key, value))
        self.items = self.items[:self.size]
        return value
    def __delitem__(self, key):
        del self.items[self.keys().index(key)]
        

_cache_fofs = Queue(10)        

class PostProcessing(with_metaclass(myMetaClass, object)):

    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]



    use_cache = True

    n_files = 10
    has_keys = False
    fof_blocks = ['MCRI','GPOS','RCRI']
    sf_blocks = ['SMST','SPOS','GRNR']
    snap_all_blocks = ['POS ','VEL ','MASS','ID  ']
    snap_gas_blocks = ['U   ','TEMP']
    subfind_and_fof_same_file = False
    subfind_files_range = None
    def fof_file(self,i_file):
        filename = '%s.%d'%(self.group_base,i_file)
        if self.use_cache and (filename in _cache_fofs.keys()):
            return _cache_fofs[filename]
        else:
            _cache_fofs[filename]=g.GadgetFile(filename, is_snap=False)
            return _cache_fofs[filename]
    def satellites(self):
        cluster_id=self.cluster_id
        keys=self.sf_blocks
        satellites={}
        just_found=False
        first_file = 0
        last_file = self.n_files+1
        if self.subfind_files_range:
            first_file = self.subfind_files_range[0]
            last_file = self.subfind_files_range[1]
        elif self.subfind_and_fof_same_file:
            first_file = self.i_file-1
            if first_file<0: first_file=0
            last_file = self.i_file+1
        else:
            first_file = 0
            last_file = self.n_files
        #print('range', (first_file, last_file+1), range(first_file, last_file+1))
        for i1_file in range(first_file, last_file+1):
            f=self.fof_file(i1_file)
            #print(f._filename)
            fof_ids=f.read_new('GRNR',1)
            #print(np.unique(fof_ids))
            if just_found==True and cluster_id not in fof_ids: 
                break
            if cluster_id in fof_ids:
                #print("!")
                if just_found is False:
                    for key in keys:
                        satellites[key]= f.read_new(key,1)[fof_ids==cluster_id] #satellites may be on different files, but always contiguous in files
                else:
                    for key in keys:
                        satellites[key]=np.concatenate((satellites[key],f.read_new(key,1)[fof_ids==cluster_id]),axis=0)
                just_found=True
        return satellites
    def header(self):
        return self.fof_file(0).header
    def box_size(self):
        return self.header().BoxSize
    def fof(self, keys=None):
        cluster_id_in_file=self.cluster_id_in_file
        i_file = self.cluster_i_file
        f=self.fof_file(i_file)
        res={}
        if keys is None:
            keys=self.fof_blocks
        for key in keys:
            res[key] = f.read_new(key,0)[cluster_id_in_file]
        #print ("cluster id in file", cluster_id_in_file)
        return res
    def z(self):
        return self.header().redshift
    def fossilness(self):
            size=self.box_size()
            cluster_center = self.fof()['GPOS']
            satellites = self.satellites()
            radius = self.rcri()
            if 'SPOS' in satellites:
                positions = satellites['SPOS']
                positions = g.periodic(positions,center=self.fof()['GPOS'],periodic=size)
                gpos= self.fof()['GPOS']
                distances = np.sqrt((positions[:,0]-gpos[0])**2.+(positions[:,1]-gpos[1])**2.+(positions[:,2]-gpos[2])**2.)
                #print(distances)
                stellar_masses = satellites['SMST'][:,4]
                
                mask_distances = distances<radius

            return fossilness(stellar_masses[mask_distances],distances[mask_distances])
    def mcri(self):   return self.fof()["MCRI"]
    def rcri(self):   return self.fof()["RCRI"]
    dm = False
    def read_new(self):
        all =  g.read_particles_in_box(self.snap_base, self.fof()['GPOS'], self.rcri(), self.snap_all_blocks+self.snap_gas_blocks,[0,1,2,3,4,5], only_joined_ptypes=False)
        gas =  all[0] #g.read_particles_in_box(self.snap_base, self.fof()['GPOS'], self.rcri(), self.snap_gas_blocks,[0])
        for k in gas:
            all[0][k]= gas[k]
        return all
    def c200c(self):
        fof_pos = self.fof()['GPOS']
        fof_r = self.fof()['RCRI']
        dm_data = self.read_new()[1]
        dm_mass_data=dm_data['MASS']
        dm_pos_data=dm_data['POS ']
        r=nfw_fit(dm_mass_data,dm_pos_data,fof_pos,fof_r)
        return O(**{"rho0":r.x[0],"c":1./r.x[1],"rs":r.x[1]*fof_r})
    def potential(self):
        return gravitational_potential(self.read_new()[-1]["MASS"], self.read_new()[-1]["POS "], self.fof()["GPOS"])
    def virialness(self):
        read_new = self.read_new()
        all_mass =read_new[-1]["MASS"]
        all_pos = read_new[-1]["POS "]
        all_vel = read_new[-1]["VEL "]
        all_potential = self.potential().potential
        gas_mass = read_new[0]["MASS"]
        gas_pos = read_new[0]["POS "]
        gas_vel = read_new[0]["VEL "]
        gas_temp = read_new[0]["TEMP"]
        gas_u = read_new[0]["U   "]
        return  virialness(self.fof()["GPOS"], self.rcri(), all_mass, all_pos, all_vel, all_potential, gas_mass, gas_pos, gas_vel, gas_u, gas_temp, H0=0.1, G=47003.1)

                

def pint():
    from pint import UnitRegistry
    u = UnitRegistry()
    u.define('Msun = 1.99885e30kg')
    u.define('cmass = 1e10 Msun/hubble') 
    u.define('clength = kpc/hubble*scale_factor5~')
    u.define('cvelocity_a = (scale_factor**0.5)*km/s')
    u.define('cvelocity_noa = km/s')
    return u
