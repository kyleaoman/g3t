#!/bin/bash
#@ job_type = parallel
#@ class = fat
#@ wall_clock_limit = 12:00:00
#@ job_name = non_di_solo_pane_vive_l_uomo
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

echo $0 
cat $0

date
