set -ev
export PROP="c200c fossilness virialness"
export TARGET=2018_sept_all_boxes_2
. sims.bash

db_1e4_ago
export MEMO=$BOXNAME$TAG

Box0mr_bao_z0;   ./ssh_launch_job.bash
Box2bhr_bao_z0;  ./ssh_launch_job.bash
Box4uhr_bao_z0;   ./ssh_launch_job.bash

#Box0mr_bao_z05;   ./ssh_launch_job.bash
#Box0mr_bao_z1;   ./ssh_launch_job.bash
#Box0mr_bao_z15;   ./ssh_launch_job.bash
#Box0mr_bao_z2;   ./ssh_launch_job.bash


#Box0mr_dm_z05;   ./ssh_launch_job.bash
#Box0mr_dm_z1;   ./ssh_launch_job.bash
#Box0mr_dm_z15;   ./ssh_launch_job.bash
#Box0mr_dm_z2;   ./ssh_launch_job.bash


#Box2bhr_bao_z05;  ./ssh_launch_job.bash
#Box2bhr_bao_z1;  ./ssh_launch_job.bash
#Box2bhr_bao_z15;  ./ssh_launch_job.bash
#Box2bhr_bao_z2;  ./ssh_launch_job.bash

#Box4uhr_bao_z05;   ./ssh_launch_job.bash
#Box4uhr_bao_z1;   ./ssh_launch_job.bash
#Box4uhr_bao_z15;   ./ssh_launch_job.bash
#Box4uhr_bao_z2; ./ssh_launch_job.bash



