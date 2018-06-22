import os
from peewee import *

print(os.environ.get('DB'))
db = SqliteDatabase(os.environ.get('DB'))

class BaseModel(Model):
    class Meta:
        database = db

class Simulation(BaseModel):
    name = TextField(unique=True)
    box_size =  FloatField(null=True)
    h =  FloatField(null=True)



class Snap(BaseModel):
    name = TextField(null=True)
    redshift =  FloatField(null=True)
    a =  FloatField(null=True)
    simulation = ForeignKeyField(Simulation, backref='snaps')
    tag = TextField(null=True)

class FoFFile(BaseModel):
    snap = ForeignKeyField(Snap, backref='foffiles')
    ifile = IntegerField()
    id_first_cluster = IntegerField()

class FoF(BaseModel):
    i_file = IntegerField()
    id_cluster = IntegerField()
    i_in_file = IntegerField()
    fsub  =  FloatField(null=True)
    m25k  =  FloatField(null=True)
    ncon  =  FloatField(null=True)
    gpos0  =  FloatField(null=True)
    gpos1  =  FloatField(null=True)
    gpos2  =  FloatField(null=True)
    m200  =  FloatField(null=True)
    goff  =  FloatField(null=True)
    lgas0  =  FloatField(null=True)
    lgas1  =  FloatField(null=True)
    lgas2  =  FloatField(null=True)
    lgas3  =  FloatField(null=True)
    lgas4  =  FloatField(null=True)
    lgas5  =  FloatField(null=True)

    ygas0  =  FloatField(null=True)
    ygas1  =  FloatField(null=True)
    ygas2  =  FloatField(null=True)
    ygas3  =  FloatField(null=True)
    ygas4  =  FloatField(null=True)
    ygas5  =  FloatField(null=True)

    tgas0  =  FloatField(null=True)
    tgas1  =  FloatField(null=True)
    tgas2  =  FloatField(null=True)
    tgas3  =  FloatField(null=True)
    tgas4  =  FloatField(null=True)
    tgas5  =  FloatField(null=True)

    mstr0  =  FloatField(null=True)
    mstr1  =  FloatField(null=True)
    mstr2  =  FloatField(null=True)
    mstr3  =  FloatField(null=True)
    mstr4  =  FloatField(null=True)
    mstr5  =  FloatField(null=True)


    start_subfind_file  =  IntegerField(null=True)
    end_subfind_file  =  IntegerField(null=True)



    mcri  =  FloatField(null=True)
    rcri  =  FloatField(null=True)
    m200  =  FloatField(null=True)
    r200  =  FloatField(null=True)
    mcon  =  FloatField(null=True)
    rcon  =  FloatField(null=True)
    m500  =  FloatField(null=True)
    r500  =  FloatField(null=True)
    m5cc  =  FloatField(null=True)
    r5cc  =  FloatField(null=True)
    mtot  =  FloatField(null=True)
    rtot  =  FloatField(null=True)
    mvir  =  FloatField(null=True)
    rvir =   FloatField(null=True)
    m25k  =  FloatField(null=True)
    r25k =   FloatField(null=True)


    glen =   IntegerField(null=True)
    nsub =   IntegerField(null=True)

    bgpo0  =  FloatField(null=True)
    bgpo1  =  FloatField(null=True)
    bgpo2  =  FloatField(null=True)

    bgma  =  FloatField(null=True)

    mgas0  =  FloatField(null=True)
    mgas1  =  FloatField(null=True)
    mgas2  =  FloatField(null=True)
    mgas3  =  FloatField(null=True)
    mgas4  =  FloatField(null=True)
    mgas5  =  FloatField(null=True)
    mgas6  =  FloatField(null=True)


    bgra  =  FloatField(null=True)
    mcri = FloatField(null=True)

    c200c = FloatField(null=True)


    fossilness_mcent = FloatField(null=True)
    fossilness_msat = FloatField(null=True)
    fossilness = FloatField(null=True)



    virialness_w = FloatField(null=True)
    virialness_es = FloatField(null=True)
    virialness_k = FloatField(null=True)
    virialness_w_gas = FloatField(null=True)
    virialness_es_gas = FloatField(null=True)
    virialness_k_gas = FloatField(null=True)
    virialness_eta = FloatField(null=True)
    virialness_beta = FloatField(null=True)
    snap = ForeignKeyField(Snap, backref='fofs')

class Galaxy(BaseModel):

    i_file = IntegerField()
    snap = ForeignKeyField(Snap, backref='galaxies')
    id_cluster = IntegerField()
    slen  =  FloatField(null=True)
    grnr = IntegerField()
    sage  =  FloatField(null=True)


    ssfr = FloatField(null=True)
    vmax = FloatField(null=True)
    dust10 = FloatField(null=True)
    spos0 = FloatField(null=True)
    spos1 = FloatField(null=True)
    spos2 = FloatField(null=True)
    dsub = FloatField(null=True)
    dust1 = FloatField(null=True)
    dust0 = FloatField(null=True)
    dust3 = FloatField(null=True)
    dust2 = FloatField(null=True)
    dust5 = FloatField(null=True)
    dust4 = FloatField(null=True)
    dust7 = FloatField(null=True)
    dust6 = FloatField(null=True)
    dust9 = FloatField(null=True)
    smst2 = FloatField(null=True)
    smst3 = FloatField(null=True)
    rhms = FloatField(null=True)
    svel0 = FloatField(null=True)
    spin1 = FloatField(null=True)
    spin0 = FloatField(null=True)
    sz   = FloatField(null=True)
    ssub = FloatField(null=True)
    svel1 = FloatField(null=True)
    scm2 = FloatField(null=True)
    svel2 = FloatField(null=True)
    rmax = FloatField(null=True)
    scm0 = FloatField(null=True)
    scm1 = FloatField(null=True)
    smst4 = FloatField(null=True)
    smst5 = FloatField(null=True)
    msub = FloatField(null=True)
    smst0 = FloatField(null=True)
    smst1 = FloatField(null=True)
    soff = FloatField(null=True)
    smhi = FloatField(null=True)
    mbid = FloatField(null=True)
    dust8 = FloatField(null=True)
    spin2 = FloatField(null=True)
    
    
tables = [Simulation,Snap,FoF,FoFFile,Galaxy]

db.create_tables(tables)
