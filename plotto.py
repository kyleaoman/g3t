import pandas as pd
import sqlite3
import contextlib 
%matplotlib notebook
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import g3read as g
import pp
u = pp.pint()



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

