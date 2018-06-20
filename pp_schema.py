import os
from peewee import *


db = SqliteDatabase(os.environ.get('DB'))

class BaseModel(Model):
    class Meta:
        database = db

    


class Simulation(BaseModel):
    name = TextField(unique=True)
    box_size =  FloatField()
    h =  FloatField()



class Snap(BaseModel):
    name = TextField()
    redshift =  FloatField()
    a =  FloatField()
    simulation = ForeignKeyField(Simulation, backref='snaps')
    tag = TextField()

class FoF(BaseModel):
    cluster_id = BigIntegerField()
    mcri = FloatField()
    rcri = FloatField()
    c200c = FloatField()


    fossilness_mcent = FloatField()
    fossilness_msat = FloatField()
    fossilness = FloatField()

    virialness_W = FloatField()
    virialness_Es = FloatField()
    virialness_K = FloatField()
    virialness_W_gas = FloatField()
    virialness_Es_gas = FloatField()
    virialness_K_gas = FloatField()
    virialness_eta = FloatField()
    virialness_beta = FloatField()
    snap = ForeignKeyField(Snap, backref='fof')

class Galaxy(BaseModel):
    galaxy_id = BigIntegerField()
    fof = ForeignKeyField(FoF, backref='galaxies')

tables = [Simulation,Snap,FoF,Galaxy]

for table in tables:
    db.create_tables([table])
