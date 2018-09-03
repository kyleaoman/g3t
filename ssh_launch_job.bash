#set -v
F=$SCRATCH/$TARGET
OUTPUT=output/$(echo $NAME|sed s,/,_,g)_${TAG}_$(echo "$PROP"|sed 's, ,_,g')
mkdir -p logs
echo OUTPUT=$OUTPUT
echo F=$F
ssh $SSH_HOST mkdir -p $F
ssh $SSH_HOST mkdir -p $F/tmp
ssh $SSH_HOST mkdir -p $F/output
rsync -arv --exclude='.*' --exclude=__pycache__ --exclude=Magneticum --cvs-exclude --exclude=output --exclude=logs --exclude=tmp .  $SSH_HOST:$F 
rsync -v --checksum $DB $SSH_HOST:$F/$TOSQL
ssh $SSH_HOST $INTRO '&&' cd $F '&&' pwd



export CHUNKS=20
export TASKS=6

function YO(){
    DA=$1
    A=$2
    CHUNKS=$3
    echo "$INTRO
cd $F
export DB=$TOSQL
seq $DA $A |
xargs -P$TASKS -n1 $MPIRUN $PYTHON composite_properties.py --basegroup $BASE/groups_$SNAP/sub_$SNAP --basesnap $BASE/snapdir_$SNAP/snap_$SNAP --simulation-name $NAME   --snap $SNAP  --chunks $CHUNKS  --prop $PROP --outfile $OUTPUT --restart $PROPFLAGS --chunk " 
}

ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 0 5 $CHUNKS)\""
ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 6 11 $CHUNKS)\""
ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 11 19 $CHUNKS)\""
#ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 15 19 $CHUNKS)\""
#ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 18 15  20)\""
#ssh $SSH_HOST $INTRO '&&' cd $F '&&' $PYTHON runjob.py -f $TEMPLATE -s $SBATCH -x "\"$(YO 16 19  20)\""

#> logs/$OUTPUT_$(date '+%Y_%m_%d_%H_%M_%S')

mkdir -p output

rsync -arv --exclude=__pycache__ --cvs-exclude  --exclude=tmp $SSH_HOST:$F/output/ output





