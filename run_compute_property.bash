set -ev
export PROP="c200c fossilness virialness"
export TARGET=2018_jul_4

#. sims.bash; Box0mr_bao_z0; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box2bhr_bao_z0; db_1e5_22j;MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
#. sims.bash; Box4uhr_bao_z0; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash

exit
. sims.bash; Box0mr_bao_z05; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box0mr_bao_z1; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box0mr_bao_z15; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box0mr_bao_z2; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash


#. sims.bash; Box0mr_dm_z0; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
#. sims.bash; Box0mr_dm_z05; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
#. sims.bash; Box0mr_dm_z1; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
#. sims.bash; Box0mr_dm_z15; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
#. sims.bash; Box0mr_dm_z2; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash



. sims.bash; Box2bhr_bao_z05; db_1e5_22j;MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box2bhr_bao_z1; db_1e5_22j;MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box2bhr_bao_z15; db_1e5_22j;MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box2bhr_bao_z2; db_1e5_22j;MEMO=$BOXNAME$TAG ./ssh_launch_job.bash




. sims.bash; Box4uhr_bao_z05; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box4uhr_bao_z1; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box4uhr_bao_z15; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash
. sims.bash; Box4uhr_bao_z2; db_1e5_22j; MEMO=$BOXNAME$TAG ./ssh_launch_job.bash


. sims.bash; Box0mr_bao_z0; bash ssh_copyback_properties.bash
