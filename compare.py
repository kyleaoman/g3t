import yaml
import yamlordereddictloader
import collections

def ureg(**defaults):
    from pint import Context
    from pint import UnitRegistry
    u = UnitRegistry()
    u.define('Msun = 1.99885e30kg')
    u.define("hubble = [hubbli]")
    u.define("scalefactor = [scalefactori]")
    u.define('cmass = 1e10 Msun/hubble')
    u.define('clength = kpc/hubble*scalefactor')
    u.define('cvelocity_a = (scalefactor**0.5)*km/s')
    u.define('cvelocity_noa = km/s')
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
                yamldata = yaml.load(stream,  Loader=yamlordereddictloader.Loader)
        elif from_yaml:
            yamldata=yaml.load(from_yaml, Loader=yamlordereddictloader.Loader)

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
                        o[key] = value
                    else:
                        o[key]= dtype(value)
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



def test():
    ot = ObservativeTable(from_csv_filename="Pratt_et_al_2016.txt")
    print(ot.z)
    print(ot.c500)
    print(ot.c500.plus)
    print(ot.c500.minus)
    print(ot.M500)
    print(ot.M500.plus)
    print(ot.M500.minus)
    import sys
    sys.exit(0)
    import cStringIO


    output = cStringIO.StringIO("""
#!/bin/sh
_global:
    M500:
        _units: "1e14 Msun"
A267:
    z: 0.227
    deltaM: 2.12
    M500:
        value: 3.60
        plus: 0.26
        minus: 0.24
    c500:
        value: 2.81
        pm: 0.28


A963:
    z: 0.206
    deltaM: 2.20
    M500: 4.82
    M500.plus: 0.58
    M500.minus: 0.52
    c500: 2.91 pm=0.28

"RXJ1720+2638":
    z: 0.164
    deltaM: 1.90
    M500: 5.26 plus=0.62 minus=0.57
    c500: 3.53 pm=0.38

"PSZ1G134.65-11.78":
    z: 0.227
    deltaM: 2.20
    M500: 5.78 plus=0.98 minus=.84
    """)

    ot = ObservativeTable(from_yaml=output)
    print(ot.z)
    print(ot.c500)
    print(ot.c500.plus)
    print(ot.c500.minus)
    print(ot.M500)
    print(ot.M500.plus)
    print(ot.M500.minus)


    ot = ObservativeTable(from_yaml_filename="example_list.yaml")
    print("z", ot.z)
    print("c500", ot.c500)
    print("c500.plus", ot.c500.plus)
    print("c500.minus", ot.c500.minus)
    print("M500", ot.M500)
    print("M500.plus", ot.M500.plus)
    print("M500.minus", ot.M500.minus)


if __name__=="__main__":
    test()

