import g3read as g
#g.debug=True
import sys
import numpy as np
import math
import json
import os



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
    import scipy
    import scipy.optimize
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
    if anz==0:
        return None
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


def resize(my_data, gpos, radius,cut=None):

    if cut is None:
        cut=radius
    for pt in my_data.keys():
        poses=my_data[pt]['POS ']
        if (len(poses))>0:
            delta=poses-gpos
            dists=np.sqrt(delta[:,0]**2+delta[:,1]**2+delta[:,2]**2)
            
            mask_dist=dists<cut
            for k in my_data[pt].keys():
                my_data[pt][k]= my_data[pt][k][mask_dist]
            my_data[pt]['DIST']=dists[mask_dist]
        else:
            my_data[pt]['DIST']=[]
    return my_data


def add_cut(my_data, gpos, cut, sample=None):
    
    for pt in my_data.keys():
        #print(pt, my_data[pt])

        poses=my_data[pt]['POS ']
        if sample is not None:
            mask_sample=np.random.choice([True,False],len(my_data[pt]["POS "]),p=[sample,1.-sample])
        if (len(poses))>0:
            delta=poses-gpos
            dists2=delta[:,0]**2+delta[:,1]**2+delta[:,2]**2
            mask_distance = dists2<(cut*cut)
            if sample is not None:
                mask = mask_sample & mask_distance
            else:
                mask = mask_distance

            for k in my_data[pt].keys():
                if len( my_data[pt][k])>0:
                        my_data[pt][k]= my_data[pt][k][mask]


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








def virialness(center, rcri, all_mass, all_pos, all_vel, all_potential, gas_mass, gas_pos, gas_vel, gas_u, gas_temp, H0=0.1, G=47003.1, cut=None, velcut=20.):

    gas =False  if (gas_mass is None or gas_vel is None or gas_pos is None) else True

    all_data={}
    all_data[-1]={}
    all_data[-1]["MASS"] = all_mass
    all_data[-1]["POS "] = all_pos
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
    #resize_order_and_sort(all_data,center,rcri,cut=cut)
    resize(all_data,center,rcri,cut=cut)
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
    Nall = all_data[-1]["MASS"].shape[0]
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
                            spherical=None,
                            cut_type=None,
                            superkeys=True, G=47003.1,
                            set_to_value_after_cut=None,
                            spher_nbs=40, spher_nfi=4, spher_nteta=4, has_keys=True):

    all_data={}
    all_data[-1]={}
    all_data[-1]["MASS"]=masses
    all_data[-1]["POS "]=positions

    if spherical is None:
        all_sferical = g.to_spherical(all_data[-1]["POS "], gpos)
    else:
        all_sferical = spherical

    all_data[-1]["SPOS"] = all_sferical

    Nall=len(all_data[-1]['MASS'])


    import math
    twopi=2.*math.pi
    pi=math.pi
    """    POTENTIAL    """
    #print all_data[-1]['SPOS']
    #print(np.min(all_data[-1]['SPOS'][:,0]),np.max(all_data[-1]['SPOS'][:,0]))
    spher_bs = [np.logspace(np.log10(np.min(all_data[-1]['SPOS'][:,0])+0.01),np.log10(np.max(all_data[-1]['SPOS'][:,0])),spher_nbs),np.linspace(0.,pi,spher_nteta), np.linspace(-pi,pi,spher_nfi)]


    mass_weights = all_data[-1]['MASS']
    if cut is not None and cut_type is not None:
        if cut_type=="sphere":
            mass_weights[all_data[-1]['SPOS'][:,0]>cut]=0.
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



    spher_all_x ,    spher_all_y ,    spher_all_z = g.to_cartesian(np.array([spher_all_cds,spher_all_cts,spher_all_cfs]).T)

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
                    position_xyz = g.to_cartesian(np.array(np.array([spher_all_cds[bin_r,bin_t,bin_phi], spher_all_cts[bin_r,bin_t,bin_phi],spher_all_cfs[bin_r,bin_t,bin_phi]])).T)
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


def spinparameter (center, rcri, all_mass, all_pos, all_vel, all_dists, gas_mass, gas_pos, gas_vel, gas_dists, G=47003.1):
    gas =False  if (gas_mass is None or gas_vel is None or gas_pos is None) else True
    gpos = center
    all_data={}
    all_data[-1]={}
    all_data[-1]["MASS"] = all_mass
    all_data[-1]["POS "] = all_pos
    all_data[-1]["VEL "] = all_vel
    #all_data[-1]["DIST"] = all_dists if all_dists is not None else g.to_spherical(all_pos, center)[:,0]
    
    if gas:
        all_data[0]={}
        all_data[0]["MASS"] = gas_mass
        all_data[0]["POS "] = gas_pos
        all_data[0]["VEL "] = gas_vel
        #all_data[0]["DIST"] = gas_dists if gas_dists is not None else g.to_spherical(gas_pos, center)[:,0]

    #print (all_data)
    for i in all_data:
        all_data[i]['MOME'] = np.zeros(all_data[i]['VEL '].shape)
        all_data[i]['MOME'][:,0] = all_data[i]['VEL '][:,0] * all_data[i]['MASS']
        all_data[i]['MOME'][:,1] = all_data[i]['VEL '][:,1] * all_data[i]['MASS']
        all_data[i]['MOME'][:,2] = all_data[i]['VEL '][:,2] * all_data[i]['MASS']
        all_data[i]['CPOS']= all_data[i]['POS ']-np.array(gpos)

    res=O()
    for i in [-1]:#all_data:

        J_vector = np.cross( all_data[i]['CPOS'], all_data[i]['MOME'] )
        J_sum = np.sum(J_vector,axis=0)
        J_modi = np.sqrt(J_sum[0]**2.+J_sum[1]**2. + J_sum[2]**2. )
        Mtot = np.sum(all_data[-1]['MASS'])
        Mtypein = np.sum(all_data[i]['MASS'])
        Lambda = J_modi*(Mtot**-1.5)*((2.*rcri)**-0.5)*(G**-0.5)
        if i==0:
            res.Lambda_0 = Lambda
            res.Jspec_0 = J_modi/Mtypein
        else:
            res.Lambda_all = Lambda
            res.Jspec_all = J_modi/Mtypein
        """
        mask_in =  all_data[i]['DIST']<(0.3*rcri)
        mask_tot_in =  all_data[-1]['DIST']<(0.3*rcri)

        r_in=0.3*rcri
        J_vector_in = np.cross(all_data[i]['CPOS'][mask_in], all_data[i]['MOME'][mask_in])
        J_sum_in = np.sum(J_vector_in,axis=0)
        J_modi_in = np.sqrt(J_sum_in[0]**2.+J_sum_in[1]**2. + J_sum_in[2]**2. )
        Mtot_in = np.sum(all_data[-1]['MASS'][mask_tot_in])
        Mtypein = np.sum(all_data[i]['MASS'][mask_in])
        Lambda_in = J_modi_in*(Mtot_in**-1.5)*((2.*r_in)**-0.5)*(G**-0.5)
        if i==0:
            res.Lambda_in_0 = Lambda_in
            res.Jspec_in_0 = J_modi_in/Mtypein
        else:
            res.Lambda_all = Lambda_in
            res.Jspec_all = J_modi_in/Mtypein
        """    
    return res


_cache_size=12


#def memo(self, maxsize=None):
def memo(maxsize=None):
    from collections import deque
    #print("memo maxsize=", maxsize)
    self = O()
    def decorator(f):
        #print("decorator self=", self, "maxsize=",maxsize)
        self.f = f
        if maxsize is not None:
            self.q = deque()
        else:
            self.q = deque(maxlen=maxsize)
        #print("q", self.q)

        def wrapper(*l,**kw):
            #print("wrapper elf",self,"q",self.q)
            #print("l",l)
            #print("kw",kw)
            myparametri=(l,kw)
            for parametri,risultato in self.q:
                if parametri == myparametri:
                    #print("found cacho ",myparametri)
                    return risultato
            #print("cacho ",myparametri)
            risultato = self.f(*myparametri[0],**myparametri[1])
            self.q.append((myparametri, risultato))
            return risultato
        return wrapper

    return decorator

@memo(maxsize=_cache_size)
def fof_info(filename, is_snap=False):
    #print("_fof info caching ",filename,is_snap)
    return g.GadgetFile(filename, is_snap)



class PostProcessing(object):

    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]



    use_cache = True

    dm = False
    n_files = 10
    has_keys = False
    fof_blocks = ['MCRI','GPOS','RCRI']
    sf_blocks = ['SMST','SPOS','GRNR','RHMS']
    snap_all_blocks = ['POS ','VEL ','MASS']#,'ID  ']
    snap_gas_blocks = ['U   ','TEMP']
    subfind_and_fof_same_file = False
    subfind_files_range = None
    random_subset_size = 2000
    myinfo=None
    @memo()
    def fof_file(self,i_file):
        global fof_info
        filename = '%s.%d'%(self.group_base,i_file)
        #print("CALL from cache", filename)
        
        f = fof_info(filename, is_snap=False)

        if f.info is not None and self.myinfo is None: 
            self.myinfo=f.info
        if f.info is None and self.myinfo is not  None:
            f.info = self.myinfo
        if f.info is None and fof_info is None:
            self.fof_file(i_file-1)
            f.info = self.myinfo
        if fof_info is None:
            raise Exception("unable to recover the fof.info block")
        return f
    @memo()
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
        i1_file=first_file-1 #, last_file+1):
        while True:
            i1_file+=1
            f=self.fof_file(i1_file)

            fof_ids=f.read_new('GRNR',1)
            #print('range', f._filename, 'fofs in file:', np.min(fof_ids), np.max(fof_ids))
            #print(f.info["GRNR"])
            #print(np.unique(fof_ids))
            if just_found==True and cluster_id not in fof_ids: 
                #print('just ofunds! & cliuster_id not in fof_ids')
                break
            if np.min(fof_ids)>cluster_id:
                #print('fof id range', np.min(fof_ids),np.max(fof_ids),'>','cluster_id',cluster_id)
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
            if np.max(fof_ids)>cluster_id:
                #print('max fof id range', np.min(fof_ids),np.max(fof_ids),'>','cluster_id',cluster_id,'next file is useless')
                break
        return satellites
    def header(self):
        return self.fof_file(0).header
    def box_size(self):
        return self.header().BoxSize
    @memo()
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
    @memo()
    def gpos(self):
        return self.fof()['GPOS']
    @memo()
    def rhms_central(self):
        satellites = self.satellites()
        if len(satellites)==0:
            return np.nan
        positions = satellites['SPOS']
        size=self.box_size()
        gpos = self.gpos()
        distances = np.sqrt((positions[:,0]-gpos[0])**2.+(positions[:,1]-gpos[1])**2.+(positions[:,2]-gpos[2])**2.)
        return satellites['RHMS'][np.argmin(distances)]
    @memo()
    def fossilness(self):
            size=self.box_size()
            cluster_center = self.gpos()
            satellites = self.satellites()
            radius = self.fof()['RCRI']
            has_satellites=False
            if 'SPOS' in satellites:
                has_satellites=True
                positions = satellites['SPOS']
                positions = g.periodic_position(positions,center=self.gpos(),periodic=size)
                gpos= self.gpos()
                distances = np.sqrt((positions[:,0]-gpos[0])**2.+(positions[:,1]-gpos[1])**2.+(positions[:,2]-gpos[2])**2.)
                #print(distances)
                if self.dm:
                    stellar_masses = satellites['SMST'][:,1]
                else:
                    stellar_masses = satellites['SMST'][:,4]
                #print(stellar_masses)
                mask_distances = distances<radius
            if has_satellites:
                return fossilness(stellar_masses[mask_distances],distances[mask_distances])
            

            return fossilness(np.nan, np.nan)
    def mcri(self):   return self.fof()["MCRI"]
    def rcri(self):   return self.fof()["RCRI"]
    @memo()
    def can_read(self):
        return os.path.exists(self.snap_base+'.0') or os.path.exists(self.snap_base)
    def fraction_cluster_match(self1, self2, distance=1000., fraction_ids=0.5, core_ids1=None):
        if core_ids1 is None:
            core_ids1=self1.core_ids()
        core_ids2= self2.core_ids()
        #print(core_ids1)
        #print(core_ids2)
        i = np.intersect1d(core_ids1, core_ids2,assume_unique=True)
        #print(len(i), max((len(core_ids1), len(core_ids2))), float(len(i))/float(max((len(core_ids1), len(core_ids2)))))
        return float(len(i))/float(max((len(core_ids1), len(core_ids2))))

    @memo()
    def core_ids(self):
        radius=self.rcri()/3.
        all_data =  self.read_new_ptypes_blocks_radius(radius=radius, blocks=  ["POS ","ID  "],ptypes=  1,join_ptypes=True,only_joined_ptypes=True)

        mask = (
        (np.abs(all_data["POS "][:,0]-self.gpos()[0])<radius) & 
        (np.abs(all_data["POS "][:,1]-self.gpos()[1])<radius) & 
        (np.abs(all_data["POS "][:,2]-self.gpos()[2])<radius) 
        )
        
        return np.sort(all_data["ID  "][mask])

    @memo()
    def read_new(self):
        if self.dm:
            blocks=self.snap_all_blocks
            ptypes=[1,2]
        else:
            blocks=self.snap_all_blocks+self.snap_gas_blocks
            ptypes=[0,1,4,5]
        all_data = self.read_new_ptypes_blocks_radius(ptypes=ptypes, blocks=blocks,  radius=self.rcri(),join_ptypes=False, only_joined_ptypes=False)
        add_cut(all_data, self.gpos(), self.rcri())
        g.join_res(all_data, blocks,  True, False)
        return all_data
    @memo()
    def read_new_ptypes_blocks_radius(self,ptypes=None, blocks=None, radius=None,join_ptypes=False, only_joined_ptypes=False):
        #print (self.dm, ptypes, blocks, self.snap_base)
        return  g.read_particles_in_box(self.snap_base, self.gpos(),
                                    radius,
                                    blocks,
                                    ptypes,
                                    join_ptypes=join_ptypes,
                                    only_joined_ptypes=only_joined_ptypes)

    @memo()
    def c200c(self):
        #print("dm?", self.dm)
        fof_pos = self.gpos()
        fof_r = self.fof()['RCRI']
        dm_data = self.read_new()[1]

        dm_mass_data=dm_data['MASS']
        dm_pos_data=dm_data['POS ']
        r=nfw_fit(dm_mass_data,dm_pos_data,fof_pos,fof_r)
        if r is not None:
            return O(**{"rho0":r.x[0],"c":1./r.x[1],"rs":r.x[1]*fof_r})
        else:
            return O(rho0=np.nan, c=np.nan, rs=np.nan)
    @memo()
    def spherical(self,ptype):
        #print (ptype, self.read_new()[ptype]['POS '])
        #print(self.read_new()[ptype])
        return  g.to_spherical(self.read_new()[ptype]['POS '],self.gpos())
    @memo()
    def potential(self):
        spherical = self.spherical(-1)
        #print("spherical", spherical)
        return gravitational_potential(self.read_new()[-1]["MASS"], 
                                       self.read_new()[-1]["POS "], 
                                       self.fof()["GPOS"], 
                                       cut=self.rcri(),
                                       cut_type="sphere",
                                       spherical=spherical
        )

    def pictures_ptypes(self):
        import matplotlib.pyplot as plt
        all_data =  self.read_new_ptypes_blocks_radius(radius= self.rcri(), blocks=  ["POS "],ptypes=  [0,1,4])
        add_cut(all_data, self.gpos(), self.rcri(),sample=0.05)
        if self.dm:
            bh_data =  {5:{"POS ":[], "MASS":[]}}
        else:
            bh_data =  self.read_new_ptypes_blocks_radius(radius= self.rcri(), blocks=  ["POS ","MASS"],ptypes=  [5])
            add_cut(bh_data, self.gpos(), self.rcri())


        f, ax = plt.subplots()
        if len(all_data[0]['POS '])>0:
            ax.scatter(all_data[0]['POS '][:,0], all_data[0]['POS '][:,1],color='red',marker='.',s=1)
        if len(all_data[1]['POS '])>0:
            ax.scatter(all_data[1]['POS '][:,0], all_data[1]['POS '][:,1],color='black',marker='.',s=1)
        if len(all_data[4]['POS '])>0:
            ax.scatter(all_data[4]['POS '][:,0], all_data[4]['POS '][:,1],color='blue',marker='.',s=1)
        if len(bh_data[5]['POS '])>0:
            ax.scatter(bh_data[5]['POS '][:,0], bh_data[5]['POS '][:,1],marker='.',s=bh_data[5]['MASS']*500.,color='yellow')

        circle2 = plt.Circle((self.gpos()[0],self.gpos()[1]), self.rcri(), color='red', fill=False)
        circle3 = plt.Circle((self.gpos()[0],self.gpos()[1]), self.rcri()/self.c200c().c, color='red', fill=False)

        #plt.xlim(prope['cluster_fof']['GPOS'][0]-prope['cluster_fof']['RCRI'], prope['cluster_fof']['GPOS'][0]+prope['cluster_fof']['RCRI'])
        #plt.ylim(prope['cluster_fof']['GPOS'][1]-prope['cluster_fof']['RCRI'], prope['cluster_fof']['GPOS'][1]+prope['cluster_fof']['RCRI'])

        ax.add_artist(circle2)
        ax.add_artist(circle3)


        #ax.set_title('%s z=%.2f'%(save_file,prope['z']))
        #print(self.z())
        ax.set_title('%s/%d z=%.2f a=%.2f'%(self.output_path, self.cluster_id, self.z(), 1./(1.+self.z())))
        ax.set_xlabel('x [kpc]')
        ax.set_ylabel('y [kpc]')
        f.savefig(self.output_path+'ptypes')


    def pictures(self):

        import matplotlib.pyplot as plt
        output_path = self.output_path
        res = self.read_new()[-1]
        n_particles = len(res["MASS"])
        ids = np.random.choice(n_particles,self.random_subset_size,replace=False)
        maskedpos = res["POS "][ids]
        fig = plt.figure()  # a new figure window
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(maskedpos[:,0],maskedpos[:,1],s=1)
        fig.savefig(output_path+'xy.png')

        fig = plt.figure()  # a new figure window
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(maskedpos[:,1],maskedpos[:,2],s=1)
        fig.savefig(output_path+'yz.png')

        fig = plt.figure()  # a new figure window
        ax = fig.add_subplot(1, 1, 1)
        ax.scatter(maskedpos[:,2],maskedpos[:,0],s=1)
        fig.savefig(output_path+'zx.png')
    @memo()
    def spinparameter(self):
        read_new = self.read_new()
        all_mass =read_new[-1]["MASS"]
        all_pos = read_new[-1]["POS "]
        all_vel = read_new[-1]["VEL "]
        if  self.dm:
            all_dists = gas_dists =  gas_mass =  gas_pos = gas_vel = None
        else:
            all_dists =        self.spherical(-1)[:,0]
            gas_dists =        self.spherical(0)[:,0]
            gas_mass = read_new[0]["MASS"]
            gas_pos = read_new[0]["POS "]
            gas_vel = read_new[0]["VEL "]

        return spinparameter (self.fof()["GPOS"], self.rcri(), all_mass, all_pos, all_vel, all_dists, gas_mass, gas_pos, gas_vel, gas_dists)

    @memo()
    def virialness(self):
        read_new = self.read_new()
        all_mass =read_new[-1]["MASS"]
        all_pos = read_new[-1]["POS "]
        all_vel = read_new[-1]["VEL "]
        all_potential = self.potential().potential
        if self.dm:
            all_dists = gas_dists =  gas_mass =  gas_pos = gas_vel = gas_u = gas_temp = None
        else:
            gas_mass = read_new[0]["MASS"]
            gas_pos = read_new[0]["POS "]
            gas_vel = read_new[0]["VEL "]
            gas_temp = read_new[0]["TEMP"]
            gas_u = read_new[0]["U   "]
        return  virialness(self.fof()["GPOS"], self.rcri(), all_mass, all_pos, all_vel, all_potential, gas_mass, gas_pos, gas_vel, gas_u, gas_temp, H0=0.1, G=47003.1)

                

from pint import Context
from pint import UnitRegistry
class O(object):
    pass 
ureg_singleton = O()
ureg_singleton.ureg=None

def ureg(**defaults):

    if ureg_singleton.ureg is None:
        u = ureg_singleton.ureg = UnitRegistry()
    else:
        return ureg_singleton.ureg
    u.define('Msun = 1.99885e30kg')
    u.define("hubble = [hubbli]")
    u.define("scalefactor = [scalefactori]")
    u.define('gmass = 1e10 Msun/hubble')
    u.define('cmass = Msun/hubble')
    u.define('clength = kpc/hubble*scalefactor')
    u.define('glength = clength')
    u.define('cvelocity = scalefactor*km/s')
    u.define('gvelocity_a = (scalefactor**0.5)km/s')
    u.define('gvelocity_noa = km/s')
    c = Context('comoving',defaults={"hubble":None,"scalefactor":None})
    def f_1(u,v,  hubble = None, scalefactor=None):
        m=v.to(u.clength).magnitude
        if hubble is not None and scalefactor is not None:
            return u.kpc*m*scalefactor/hubble
        else:
            raise Exception("hubble=%s, scalefactor=%s"%(str(hubble), str(scalefactor)))
    def f_2(u,v,  hubble = None, scalefactor=None):
        m=v.to(u.kpc).magnitude
        if hubble is not None and scalefactor is not None:
            return u.clength/scalefactor*hubble
        else:
            raise Exception("hubble=%s, scalefactor=%s"%(str(hubble), str(scalefactor)))
    c.add_transformation('[length] * [scalefactori] / [hubbli]', '[length]',f_1)
    c.add_transformation('[length]','[length] * [scalefactori] / [hubbli]', f_2)
    u.add_context(c)
    if(len(defaults)>0):
        u.enable_contexts(c,**defaults)

    return u

