#set -v
F=$SCRATCH/$TARGET
echo F=$F
ssh $SSH_HOST mkdir -p $F
ssh $SSH_HOST mkdir -p $F/tmp
ssh $SSH_HOST mkdir -p $F/output
rsync -arv --exclude='.*' --exclude=__pycache__ --exclude=Magneticum --cvs-exclude --exclude=output --exclude=logs --exclude=tmp .  $SSH_HOST:$F 
rsync -v --checksum $DB $SSH_HOST:$F/$TOSQL
ssh $SSH_HOST $INTRO '&&' cd $F '&&' pwd
OUTPUT=output/$MEMO$(echo $NAME|sed s,/,_,g)_$PROP
mkdir -p logs

export CHUNKS=20
export TASKS=5

ssh $SSH_HOST $INTRO '&&' cd $F '&&'  seq 0 $((CHUNKS-1))  '|' DB=$TOSQL xargs -P$TASKS -n1   $PYTHON composite_properties.py --basegroup $BASE/groups_$SNAP/sub_$SNAP --basesnap $BASE/snapdir_$SNAP/snap_$SNAP --simulation-name $NAME   --snap $SNAP  --chunks $CHUNKS  --prop $PROP --outfile $OUTPUT --restart --chunk > logs/$OUTPUT_$(date '+%Y_%m_%d_%H_%M_%S')
mkdir -p output
rsync -arv --exclude=__pycache__ --cvs-exclude  --exclude=tmp $SSH_HOST:$F/output/ output





