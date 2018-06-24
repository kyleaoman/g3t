#!/bin/bash
#@ job_type = parallel
#@ class = fat
#@ wall_clock_limit = 24:00:00
#@ job_name = non
#@ node = 1
#@ tasks_per_node = 1
#@ output = job_$(jobid).out
#@ error = job_$(jobid).err
#@ group = pr86re
#@ node_usage = shared
#@ resources = ConsumableCpus(1)
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

date
