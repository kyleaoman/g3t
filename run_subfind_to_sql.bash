#set -v
set -ve
#rm $DB && python subfind_to_sql.py  --ciao 2>/dev/null

echo DB=$DB
if [ -z "$DB" ]; then echo 'no $DB set'; exit;fi

python subfind_to_sql.py || true
#sqlite3 $DB 'CREATE INDEX fof_i  ON fof (snap_id,id_cluster);' || true
#sqlite3 $DB 'CREATE INDEX galaxy_i  ON galaxy (snap_id,id_cluster);' || true
#sqlite3 $DB 'CREATE INDEX galaxy_i_pos  ON galaxy (snap_id,id_cluster,spos0,spos1,spos2);' || true
#sqlite3 $DB '.index' || true

echo NAME=$NAME LIM=$LIM   TAG=$TAG SNAP=$SNAP 

python subfind_to_sql.py  --basename $NAME/  --snap $SNAP --simulation-name $NAME --tag $TAG --min-val $LIM --add-fof 1 --delete-groups 1


SNAP_ID=$(sqlite3 $DB "
SELECT snap.id FROM snap 
inner join simulation on snap.simulation_id=simulation.id 
where simulation.name='$NAME' and snap.tag='$TAG'
")

echo SNAP_ID=$SNAP_ID

sqlite3 $DB "
delete from fof 
where fof.snap_id='$SNAP_ID' AND  mcri<(
    select MAX(mcri) from fof 
    where  fof.snap_id='$SNAP_ID' AND glen<(
        select MIN(GLEN) from fof  
        where fof.snap_id='$SNAP_ID'
    )*1.1
)
"

python subfind_to_sql.py  --basename $NAME  --snap $SNAP --simulation-name $NAME --tag $TAG  --add-fof 0 --add-sf-bounds 1

#python subfind_to_sql.py  --basename $NAME  --snap $SNAP --simulation-name $NAME --tag $TAG  --add-fof 0 --add-sf-bounds 0 --add-sf-data  1 --only-subfind-existing-columns
