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
ssh $SSH_HOST $INTRO '&&' cd $F '&&' DB=$TOSQL $PYTHON composite_properties.py --basegroup $BASE/groups_$SNAP/sub_$SNAP --basesnap $BASE/snapdir_$SNAP/snap_$SNAP --simulation-name $NAME   --snap $SNAP --chunk 0 --chunks 10  --prop $PROP #'>' $OUTPUT








