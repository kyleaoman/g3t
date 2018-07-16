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
from pint import Context
from pint import UnitRegistry
    
import pandas as pd
import pp
ureg = pp.ureg


class O(object):
    def __init__(self, **kw):
        for k in kw:
            self.__dict__[k]=kw[k]
    pass

import numpy as np
import matplotlib.units 
class SubclassedSeries(pd.Series):

    @property
    def _constructor(self):
        return SubclassedSeries

    @property
    def _constructor_expanddim(self):
        return SubclassedDataFrame

class SubclassedDataFrame(pd.DataFrame):

    @property
    def _constructor(self):
        return SubclassedDataFrame

    @property
    def _constructor_sliced(self):
        return SubclassedSeries
    
#    def __init__(self,*l,**kw):
#        super(Ciaos, self).__init__(*l, **kw)
        

        
class MyArray(np.ndarray):

    def __new__(cls, value):
        return np.asarray(value).view(cls)

    def __array_finalize__(self, obj):
        if obj is None: 
            return


    def __array_wrap__(self, out_arr, context=None):
        return out_arr

def isfloat(val):
    return all([ [any([i.isnumeric(), i in ['.','e']]) for i in val],  len(val.split('.')) == 2] )

class ObservativeTable(object):
    def __new__(self,  
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
                 dollar=':'):
        #print(self)
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
            yamldata=self.read_csv_reader(self, from_csv_reader)


        elif from_csv_filename:
            import csv
            dict1 = {}
            dialect = None
            with open(from_csv_filename, "r") as infile:
                if csv_delimiter:
                    reader = csv.reader(infile, delimiter=csv_delimiter)
                elif csv_delimiter_and_skip:
                    
                    reader = csv.reader(infile, skipinitialspace=True, delimiter=csv_delimiter_and_skip)
                yamldata=self.read_csv_reader(self, reader)


        elif from_yaml_filename:
            
            yamldata=None
            
            with open(from_yaml_filename, 'r') as stream:
                yamldata = yaml.load(stream)#,  Loader=yamlordereddictloader.Loader)
        elif from_yaml:
            yamldata=yaml.load(from_yaml)#, Loader=yamlordereddictloader.Loader)

        yamldata = self.make_ot_from_yaml(self, yamldata)
        return self.load(self, yamldata)
    def read_csv_reader(self, reader):
        import json
        _headers = next(reader)
        headers=[]
        for _head in _headers:
            _head = _head.strip()
            if _head[0]=='#':
                _head = _head[1:]
            if len(_head)==0:
                continue
            headers.append(_head)
        
        dict1 = list()
        globy = {self._uid:"_global"}
        dict1.append(globy)
        actual_rows = 0
        for row in reader:
            if len(row)==0:
                continue
            #print(row, len(row), len(row[0]))
            if len(row[0])>0 and row[0][0] =='#':
                if actual_rows>0:
                    continue
                comment = ' '.join(row)[1:]

                j = yaml.load(comment)

                if len(j)>0:
                    newj=globy
                    for key in j:
                        value = j[key]
                        if self.dot in key:
                            supkey, subkey = key.split(self.dot,1)
                            if supkey not in newj:
                                newj[supkey]={}
                            newj[supkey][subkey] = value
                        else:
                            newj[key]=value
                    #print(newj)
                    globy.update(newj)
                    


            else:
                #print(row, headers)
                dtype = float
                o={}
                for key, value in zip(headers, row):
                    keysvalues={}
                    #print('keyvalue', key, value)
                    if self.dollar in value:
                        if globy and key not in globy:
                            globy[key]={}
                        if "_dtype" not in globy[key]:
                            globy[key]["_dtype"]='float'
                            #print(value, self.dollar in value)
                        for subkeyvalue in value.split():
                            if self.dollar in subkeyvalue:
                                subkey,subvalue = subkeyvalue.split(self.dollar)
                                keysvalues[key+'.'+subkey]=subvalue
                            else:
                                keysvalues[key]=subkeyvalue
                    else:
                        keysvalues[key]=value
                    #print(globy)
                    for subkey in keysvalues:
                        value = keysvalues[subkey].strip()
                        dtype = float
                        #print(value)
                        if value =='':
                             o[ subkey]=np.nan
                        elif globy and key in globy and "_dtype" in globy[key]:
                            
                            dtype=np.__dict__[globy[key]["_dtype"]]
                            #print('value:')
                            #print(value)
                            if '_nan_on_error' in globy and globy['_nan_on_error']:
                                try:
                                    o[ subkey]=np.array(value, dtype=dtype)
                                except:
                                    o[ subkey]=np.nan
                            else:
                                o[ subkey]=np.array(value, dtype=dtype)
                            
                            #print("1", dtype)
                        elif not isfloat(value):
                            if key not in globy:
                                
                               globy[key]={}
                            #print("value is not float", value)
                            globy[key]["_dtype"] = "object"
                            dtype=str
                            o[ subkey] = value
                            #print("2")
                            
                        else:
                            

                            o[subkey] =  np.array(value, dtype=dtype)
                            #print("3",dtype)
                dict1.append(o)
                actual_rows += 1
        #print(globy)      
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
        self.new_column(self, column_name, subcolumn_name)
        mypos = self.columns[column_name][self._uid]==myid

        try:


            self.columns[column_name][subcolumn_name][mypos] = value
        except:

            raise Exception("Impossible to add value %s to column '%s'.'%s'.'%s'"%(str(value), column_name, subcolumn_name, str(mypos)))
        if subcolumn_name == "pm":
            self.append(self, column_name, "p", myid, value)
            self.append(self, column_name, "m", myid, value)

        if subcolumn_name == "p":
            self.append(self, column_name, "plus", myid, value)

        if subcolumn_name == "m":
            self.append(self, column_name, "minus", myid, value)


    def new_column(self, column_name, subcolumn_name  ):
        #
        dtype=np.float32
        #print("    new_column", column_name, "subc", subcolumn_name)
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
        #print(data)
        if '_global' in data:
            self.glob.update(data['_global'])
        self.object_names = []
        for object_name in data:
            if object_name[0]==self.underscore:
                continue
            self.object_names.append( object_name)
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
                self.new_column(self, column_name, None)

                if self.dot in key:
                    subcolumn_name = key.split(self.dot,1)[1]
                    self.append(self, column_name, subcolumn_name, object_name, value)
                else:
                    #print("else:", data[object_name][key],data[object_name][key].__class__)
                    if isinstance(data[object_name][key], dict):
                        #print("A")
                        for subcolumn_name in data[object_name][key]:
                            
                            self.append(self, column_name, subcolumn_name, object_name,  value[subcolumn_name])
                    elif isinstance(data[object_name][key], str):
                        #print("N")
                        subvalues = value.split()
                        #print("else ->", data[object_name][key], subvalues)
                        for subkeyvalue_withspaces in subvalues:
                            subkeyvalue = subkeyvalue_withspaces.strip()
                            #print("            subkeyvalue", subkeyvalue, self.dollar not in subkeyvalue)
                            if self.dollar not in subkeyvalue:
                                subkey = "value"
                                subvalue = subkeyvalue
                            else:
                                subkey, subvalue = subkeyvalue.strip().split(self.dollar,1)
                            self.append(self, column_name, subkey, object_name,  subvalue)
                    else:
                        #print("C")
                        self.append(self, column_name, "value", object_name, value)
        
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
            #print(mya)
            col =  convert(mya)
            col._convert = convert
            self.columns[column_name]['value']=col
            for subcol in self.columns[column_name]:
                if subcol=="value":
                    continue
                else:
                    c=subcol!=self._uid
                    d=subcol[0]!=self.underscore
                    #print(column_name,"subcol", subcol, "self._uid", self._uid, " subcol!=self._uid",c,"subcol[0]!=self.underscore",d)
                    if d and c:
                            self.columns[column_name][subcol] = convert(self.columns[column_name][subcol])
                    else:
                        if not isinstance(factor, float) and subcol!="_units":
                            self.columns[column_name][subcol] = self.columns[column_name][subcol]
                            pass
            self.columns[column_name]
        #print(data)
        sorted_keys = sorted(self.columns.keys())
        subsorted_keys = ['value','plus','minus']
        labels1 = []
        labels2 = []
        isorted=-1
        rdataset = []
        for sorted_key in sorted_keys:
            isorted+=1
            isubsorted=-1
            for subsorted_key in subsorted_keys:
                isubsorted+=1
                if subsorted_key in self.columns[sorted_key] :
                    labels1.append(isorted)
                    labels2.append(isubsorted)
        
        for irow in range(len(self.columns[sorted_keys[0]]['value'])):
            row = []
            for sorted_key in sorted_keys:
                for subsorted_key in subsorted_keys:
                    if subsorted_key in self.columns[sorted_key] :
                        #print(self.columns[sorted_key][subsorted_key][irow])
                        row.append(self.columns[sorted_key][subsorted_key][irow])
            rdataset.append(row)

        mindex = pd.MultiIndex(
                levels=[sorted_keys, subsorted_keys],
                labels=[labels1, labels2]
         )

        df = SubclassedDataFrame(rdataset, columns=mindex)
        """for column in df:
                df[column]=Ciaos(df[column])
                print(Ciaos,'->',df[column].__class__)"""
        #print(df)
        return df
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



   

def gen_supermap(data, poutside=0.02):
        from matplotlib.colors import LinearSegmentedColormap
        lscm=None
      
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

    

import io, os, sys, types

from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']
    for d in path:
        nb_path = os.path.join(d, name + ".ipynb")
        if os.path.isfile(nb_path):
            return nb_path
        # let import Notebook_Name find "Notebook Name.ipynb"
        nb_path = nb_path.replace("_", " ")
        if os.path.isfile(nb_path):
            return nb_path


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""
    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print ("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)


        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = types.ModuleType(fullname)
        mod.__file__ = path
        mod.__loader__ = self
        mod.__dict__['get_ipython'] = get_ipython

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        if True:#try:
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    code = self.shell.input_transformer_manager.transform_cell(cell.source)
                    #print("code:",code)
                    #print(mod.__dict__)
                    exec(code, mod.__dict__)
        #finally:
            self.shell.user_ns = save_user_ns
        sys.modules[fullname] = mod
        return mod

    
    
class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""
    def __init__(self):
        self.loaders = {}

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        if key not in self.loaders:
            self.loaders[key] = NotebookLoader(path)
        return self.loaders[key]

import sys
sys.meta_path.append(NotebookFinder())


import matplotlib.units

import pint

class PintAxisInfo(matplotlib.units.AxisInfo):
    """Support default axis and tick labeling and default limits."""

    def __init__(self, units):
        """Set the default label to the pretty-print of the unit."""
        #print("untis," ,units)
        if units is not None:
            super(PintAxisInfo, self).__init__(label='{:P}'.format(units))
        else:
            super(PintAxisInfo, self).__init__()


class PintConverter(matplotlib.units.ConversionInterface):
    """Implement support for pint within matplotlib's unit conversion framework."""

    def __init__(self, registry):
        super(PintConverter, self).__init__()
        self._reg = registry

    def convert(self, value, unit, axis):
        """Convert :`Quantity` instances for matplotlib to use."""
        if isinstance(value, (tuple, list)):
            return [self._convert_value(v, unit, axis) for v in value]
        else:
            return self._convert_value(value, unit, axis)

    def _convert_value(self, value, unit, axis):
        #print("self", self)
        #print("value", value)
        #print("unit", unit)
        #print("axis", axis)
        """Handle converting using attached unit or falling back to axis units."""
        if hasattr(value, 'units'):
            return value.to(unit).magnitude
        else:
            if unit is not None:
                return self._reg.Quantity(value, axis.get_units()).to(unit).magnitude
            else:
                #print(value)
                return value

    @staticmethod
    def axisinfo(unit, axis):
        """Return axis information for this particular unit."""
        #print("untis," ,unit, "axis",axis)
        return PintAxisInfo(unit)

    @staticmethod
    def default_units(x, axis):
        """Get the default unit to use for the given combination of unit and axis."""
        return getattr(x, 'units', None)

import pandas as pd
# Register the class
matplotlib.units.registry[SubclassedSeries] = PintConverter(ureg())
matplotlib.units.registry[ureg().Quantity] = PintConverter(ureg())

#munits.registry[pd.core.series.Series] = PintConverter(ureg())

