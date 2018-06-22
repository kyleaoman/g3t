SSH_HOST='di29bop2@c2paplogin.lrz.de'
INTRO="module load python/3.5_anaconda_nompi"
SCRATCH=/gpfs/work/pr86re/di29bop2
BASE=/smgpfs/work/pr83li/lu78qer5/Magneticum/Box0/mr_bao
TARGET=ciao2
SQL=/tmp/ciao_1e4_22_06_2018.sql
TOSQL=tmp/ciao.sql
PYTHON=python3
NAME=/HydroSims/Magneticum/Box0/mr_bao/ 
SNAP=037
PROP=c200c

set -v
F=$SCRATCH/$TARGET
ssh $SSH_HOST mkdir -p $F
ssh $SSH_HOST mkdir -p $F/tmp
ssh $SSH_HOST mkdir -p $F/output
rsync -arv --exclude=__pycache__ --cvs-exclude --exclude=output --exclude=tmp .  $SSH_HOST:$F 
rsync -v --checksum $SQL $SSH_HOST:$F/$TOSQL
ssh $SSH_HOST $INTRO '&&' cd $F '&&' find
OUTPUT=output/$(echo $NAME|sed s,/,_,g)_$PROP
echo ssh $SSH_HOST $INTRO '&&' cd $F '&&' DB=$TOSQL $PYTHON composite_properties.py --basegroup $BASE/groups_$SNAP/sub_$SNAP --basesnap $BASE/snapdir_$SNAP/snap_$SNAP --simulation-name $NAME   --snap $SNAP --chunk 0 --chunks 10  --prop $PROP '>' $OUTPUT
ssh $SSH_HOST $INTRO '&&' cd $F '&&' DB=$TOSQL $PYTHON composite_properties.py --basegroup $BASE/groups_$SNAP/sub_$SNAP --basesnap $BASE/snapdir_$SNAP/snap_$SNAP --simulation-name $NAME   --snap $SNAP --chunk 0 --chunks 10  --prop $PROP '>' $OUTPUT








