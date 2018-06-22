set -v
#rm ciao.sql
export DB=/tmp/ciao_1e4_22_06_2018.sql
export LIM=1e4

#rm $DB && python subfind_to_sql.py  --ciao 2>/dev/null

sqlite3 $DB 'CREATE INDEX fof_i  ON fof (snap_id,id_cluster);' 2>/dev/null
sqlite3 $DB 'CREATE INDEX galaxy_i  ON fof (snap_id,id_cluster);' 2>/dev/null
sqlite3 $DB '.index' 

function insert(){
    echo NAME=$NAME LIM=$LIM   TAG=$TAG SNAP=$SNAP 



    python subfind_to_sql.py  --basename $NAME/  --snap $SNAP --simulation-name $NAME --tag $TAG --min-val $LIM --add-fof 1

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
#    python subfind_to_sql.py  --basename $NAME  --snap $SNAP --simulation-name $NAME --tag $TAG  --add-fof 0 --add-sf-bounds 0 --add-sf-data  1
}
snapz2="010"
snapz15="012"
snapz05="025"
snapz1="014"
snapz0="037"

NAME=/HydroSims/Magneticum/Box0/mr_bao/  TAG=z0 SNAP=037 insert
NAME=/HydroSims/Magneticum/Box0/mr_bao/  TAG=z05 SNAP=025  insert
NAME=/HydroSims/Magneticum/Box0/mr_bao/  TAG=z1 SNAP=014 insert
NAME=/HydroSims/Magneticum/Box0/mr_bao/  TAG=z15 SNAP=012 insert
NAME=/HydroSims/Magneticum/Box0/mr_bao/  TAG=z2 SNAP=010 insert

