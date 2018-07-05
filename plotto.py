import yaml
#import yamlordereddictloader
import collections
import pandas as pd
import sqlite3
import contextlib 
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import g3read as g



def ureg(**defaults):
    from pint import Context
    from pint import UnitRegistry
    u = UnitRegistry()
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


class O(object):
    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]
    pass

import numpy as np

class MyArray(np.ndarray):

    def __new__(cls, value):
        return np.asarray(value).view(cls)

    def __array_finalize__(self, obj):
        if obj is None: 
            return


    def __array_wrap__(self, out_arr, context=None):
        super(MyArray, self).__array_wrap__(self, out_arr, context)
        return out_arr

def isfloat(val):
    return all([ [any([i.isnumeric(), i in ['.','e']]) for i in val],  len(val.split('.')) == 2] )

class ObservativeTable(object):
    def __init__(self,  
                 from_csv_filename = None,
                 from_csv_reader = None,
                 csv_delimiter_and_skip=' ',
                 csv_delimiter=None,
                 from_yaml = None,
                 from_yaml_filename=None,
                 dot='.',
                 underscore='_', 
                 _uid="id",
                 uregistry=None, 
                 dollar='='):
        self.glob = {}
        self.dollar=dollar
        self.ureg = ureg()
        self._uid = _uid
        self.dot=dot
        self.underscore=underscore
        if uregistry is None:
            self.ureg = ureg()
        else:
            self.ureg = uregistry
        if from_csv_reader:
            yamldata=self.read_csv_reader(from_csv_reader)


        elif from_csv_filename:
            import csv
            dict1 = {}
            dialect = None
            with open(from_csv_filename, "r") as infile:
                if csv_delimiter:
                    reader = csv.reader(infile, delimiter=csv_delimiter)
                if csv_delimiter_and_skip:
                    
                    reader = csv.reader(infile, skipinitialspace=True, delimiter=csv_delimiter_and_skip)
                yamldata=self.read_csv_reader(reader)


        elif from_yaml_filename:
            
            yamldata=None
            
            with open(from_yaml_filename, 'r') as stream:
                yamldata = yaml.load(stream)#,  Loader=yamlordereddictloader.Loader)
        elif from_yaml:
            yamldata=yaml.load(from_yaml)#, Loader=yamlordereddictloader.Loader)

        yamldata = self.make_ot_from_yaml(yamldata)
        self.load(yamldata)
    def read_csv_reader(self, reader):
        import json
        headers = next(reader)
        headers[0] = headers[0][1:]
        dict1 = list()
        globy = {self._uid:"_global"}
        dict1.append(globy)
        for row in reader:
            if len(row)==0:
                    continue
            if row[0][0] =='#':
                comment = ' '.join(row)[1:]

                j = yaml.load(comment)

                if len(j)>0:
                    newj={}
                    for key in j:
                        value = j[key]
                        if self.dot in key:
                            supkey, subkey = key.split(self.dot,1)
                            if supkey not in newj:
                                newj[supkey]={}
                            newj[supkey][subkey] = value
                        else:
                            newj[key]=value
                    globy.update(newj)
                    


            else:
                dtype = float
                o = {}
                for key, value in zip(headers, row):
                    dtype = float

                    if globy and key in globy and "_dtype" in globy[key]:
                        dtype=np.__dict__[globy[key]["_dtype"]]
                    elif not isfloat(value):
                        if key not in globy:
                               globy[key]={}
                        globy[key]["_dtype"]="object"
                        dtype=np.object
                    
                    o[key]= np.array(value, dtype=dtype)
                dict1.append(o)

        return dict1
    def make_ot_from_yaml(self, yamldata):
        if isinstance(yamldata, list):
            res = collections.OrderedDict({})
            row=0
            for item in yamldata:
                row=row+1

                if self._uid in item:

                    uid = item[self._uid]
                    if uid in res:
                        raise Exception("duplicate id %s"%uid)
                    res[uid] = item
                else:
                    
                    while str(row) in res:
                        row=row+1
                    res[str(row)]=item
            return res
        if isinstance(yamldata, dict):
            return yamldata
    def append(self, column_name, subcolumn_name, myid, value):
        #
        self.new_column(column_name, subcolumn_name)
        mypos = self.columns[column_name][self._uid]==myid

        try:


            self.columns[column_name][subcolumn_name][mypos] = value
        except:

            raise Exception("Impossible to add value %s to column '%s'.'%s'.'%s'"%(str(value), column_name, subcolumn_name, str(mypos)))
        if subcolumn_name == "pm":
            self.append(column_name, "p", myid, value)
            self.append(column_name, "m", myid, value)

        if subcolumn_name == "p":
            self.append(column_name, "plus", myid, value)

        if subcolumn_name == "m":
            self.append(column_name, "minus", myid, value)


    def new_column(self, column_name, subcolumn_name = None):
        #
        dtype=np.float32
        if column_name in self.glob and "_dtype" in self.glob[column_name]:
            dtype = np.__dict__[self.glob[column_name]["_dtype"]]
        if column_name not in self.columns:
            #print("    new_column", column_name)
            self.columns[column_name]={"value":np.full(self.n_objects,np.nan, dtype),
                                       "_units":1.,self._uid:np.array(self.object_names,dtype=object),
                                       '_dtype':dtype}

            if column_name in self.glob:
                for default_subcolumn_name in self.glob[column_name]:
                    if default_subcolumn_name[0]==self.underscore:
                        self.columns[column_name][default_subcolumn_name] = self.glob[column_name][default_subcolumn_name]
                    else:
                        self.columns[column_name][default_subcolumn_name] = np.full(self.n_objects, np.nan, dtype=dtype)
        if subcolumn_name is not None and subcolumn_name not in self.columns[column_name]:

            self.columns[column_name][subcolumn_name] = np.full(self.n_objects, np.nan, dtype = dtype)

    def load(self, data):
        if '_global' in data:
            self.glob.update(data['_global'])
        self.object_names = []
        for object_name in data:
            if object_name[0]==self.underscore:
                continue
            self.object_names.append(object_name)
        self.n_objects = len(self.object_names)
        self.columns={}
        for object_name in self.object_names:
            #print("object_name: ", object_name)
            for key in data[object_name]:
                subcolumn_names = []
                value = data[object_name][key]
                if self.dot in key:
                    column_name = key.split(self.dot,1)[0]
                else:
                    column_name = key
                self.new_column(column_name)

                if self.dot in key:
                    subcolumn_name = key.split(self.dot,1)[1]
                    self.append(column_name, subcolumn_name, object_name, value)
                else:
                    if isinstance(data[object_name][key], dict):
                        for subcolumn_name in data[object_name][key]:
                            
                            self.append(column_name, subcolumn_name, object_name,  value[subcolumn_name])
                    elif isinstance(data[object_name][key], str):
                        subvalues = value.split()
                        for subkeyvalue_withspaces in subvalues:
                            subkeyvalue = subkeyvalue_withspaces.strip()
                            #print("            subkeyvalue", subkeyvalue, self.dollar not in subkeyvalue)
                            if self.dollar not in subkeyvalue:
                                subkey = "value"
                                subvalue = subkeyvalue
                            else:
                                subkey, subvalue = subkeyvalue.strip().split(self.dollar,1)
                            self.append(column_name, subkey, object_name,  subvalue)
                    else:
                        self.append(column_name, "value", object_name, value)
        for column_name in self.columns:
            mya = MyArray(self.columns[column_name]["value"])
            factor=1.
            convert = lambda x:x
            if "_units" in self.columns[column_name] and isinstance(self.columns[column_name]["_units"], str):
                factor = self.ureg.parse_expression(self.columns[column_name]["_units"])
                convert =  lambda mya: factor.units*factor.magnitude * mya 

            elif "_units" in self.columns[column_name] and  mya.dtype==float:
                factor = self.columns[column_name]["_units"]
                convert = lambda mya: mya*factor

            col =  convert(mya)
            col._convert = convert
            for subcol in self.columns[column_name]:
                if subcol=="value":
                    continue
                else:
                    c=subcol!=self._uid
                    d=subcol[0]!=self.underscore
                    #print(column_name,"subcol", subcol, "self._uid", self._uid, " subcol!=self._uid",c,"subcol[0]!=self.underscore",d)
                    if d and c:
                            col.__dict__[subcol] = convert(self.columns[column_name][subcol])
                    else:
                        if not isinstance(factor, float) and subcol!="_units":
                            col.__dict__[subcol] = self.columns[column_name][subcol]
                            pass
            
            self.__dict__[column_name] = col
        del self.glob
        del self.columns

def query(DB):
    def simul(q):
        with contextlib.closing(sqlite3.connect(DB)) as con:
            with con as cur:
               return pd.read_sql_query(q, cur)
    return simul

def supermap(df, f, p=0.005):
    n = len(df.index)
    fn = int(n*p)    
    largest  = f.nlargest(fn).tail(1).values[0]
    smallest  = f.nsmallest(fn).tail(1).values[0]
    return df.where(f<largest).where(f>smallest*1.1).where(f!=np.nan), df.where((f>largest)|(f<smallest*1.1)|(f==np.nan))

def plot_f(ax, xmin, xmax, f, bins=20,logscale=True):
    if logscale:
        xs = np.logspace(np.log10(xmin), np.log10(xmax), bins)
    else:
        xs = np.linspace(xmin, xmax, bins)
    vfunc = np.vectorize(f)
    ax.plot(xs,vfunc(xs))



   

def gen_supermap(data):
        from matplotlib.colors import LinearSegmentedColormap
        lscm=None
        poutside=0.02
        all_c = data
        maska=(~np.isnan(all_c)) & (all_c>0.)
        all_c = all_c[maska]
        ordered_c = np.sort(np.log10(all_c))

        npoints = int(len(all_c)*poutside)
        prima_mini = ordered_c[0]
        prima_maxi = ordered_c[-1]

        prima_interval=prima_maxi-prima_mini
        confident_points = ordered_c[npoints:-npoints]


        if len(confident_points)>0:
            dopo_mini=confident_points[0]
            shift_mini=dopo_mini-prima_mini
            dopo_maxi=confident_points[-1]
            shift_maxi=-(dopo_maxi-prima_maxi)

            mini_frac=float(shift_mini)/float(prima_interval)
            maxi_frac=1.-float(shift_maxi)/float(prima_interval)

            
            w=[0.,mini_frac,mini_frac+1.*(maxi_frac-mini_frac)/5.,mini_frac-(2.)*(mini_frac-maxi_frac)/5.,mini_frac-(3.)*(mini_frac-maxi_frac)/5.,mini_frac-(3.9)*(mini_frac-maxi_frac)/5.,maxi_frac,1.0]

            cdict =  {'red':   ((w[0], 0, 0),
                        (w[1], 0, 0),
                        (w[3], 0, 0),
                        (w[4], 1, 1),
                        (w[5], 1, 1),
                         (w[6], 0.5, 0.1),
                        (w[7], 0.1, 0.1)),
             'green': ((w[0], 0, 0),
                       (w[1], 0, 0),
                        (w[2], 0, 0),
                        (w[3], 1, 1),
                        (w[4], 1, 1),
                        (w[5], 0, 0),
                        (w[6], 0, 0),
                        (w[7], 0, 0)),
              'blue':  ((w[0], 0.1, 0.1),
                       (w[1], 0.5, 0.5),
                       (w[2], 1, 1),
                       (w[3], 1, 1),
                        (w[4], 0, 0),
                       (w[5], 0, 0),
                        (w[6], 0, 0),
                        (w[7], 0, 0))}


            lscm = LinearSegmentedColormap('BlueRed1', cdict)
        else:
            cdict = cdict1 = {'red':   ((0.0, 0.0, 0.0),
                   (0.5, 0.0, 0.1),
                   (1.0, 1.0, 1.0)),

         'green': ((0.0, 0.0, 0.0),
                   (1.0, 0.0, 0.0)),

         'blue':  ((0.0, 0.0, 1.0),
                   (0.5, 0.1, 0.0),
                   (1.0, 0.0, 0.0))
        }
            lscm = LinearSegmentedColormap('BlueRed1', cdict)
        norm=matplotlib.colors.LogNorm(vmin=all_c.min(), vmax=all_c.max())
        cmap=cmap=lscm
        cmap.set_bad('white')
        return cmap,norm
