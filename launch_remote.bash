SSH_HOST='di29bop2@supermuc.lrz.de'
INTRO="module load python/3.5_anaconda_nompi"
SCRATCH=/gpfs/work/pr86re/di29bop2
BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao
TARGET=ciao
SQL=/tmp/ciao_1e4_22_06_2018.sql
PYTHON=python3

set -v
F=$SCRATCH/$TARGET
ssh $SSH_HOST mkdir -p $F
rsync -arv --cvs-exclude --checksum --exclude=output .  $SSH_HOST:$F 
ssh $SSH_HOST $INTRO '&&' $PYTHON -mpip install peewee --user
ssh $SSH_HOST $INTRO '&&' $PYTHON composite_properties.py






