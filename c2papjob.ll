#!/bin/bash
#@ job_type = parallel
#@ class = parallel
#fat
#@ wall_clock_limit = 24:00:00
#@ job_name = nograzie
#@ node = 1
#@ tasks_per_node = 4
#@ output = job_$(jobid).out
#@ error = job_$(jobid).err
#@ group = pr86re
#@ node_usage = shared
#@ resources = ConsumableCpus(4)
#@ queue

. /etc/profile
. /etc/profile.d/modules.sh

module load idl
module load idl 2>/dev/null
module unload python 2>/dev/null
module unload mpi.ibm 2>/dev/null

#module load python/2.7_anaconda_mpi

echo $0
cat $0

echo hostname:
hostname

echo hostnames:
mpirun hostname

date
