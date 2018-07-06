set -ev
. sims.bash; Box4uhr_bao_z0; db_1e5_22j; 
echo $INTRO
. sims.bash;  db_1e5_22j

PROPS="c200c_fossilness_virialness"
CSV_COLS="c200c_c c200c_rho0 c200c_rs fossilness_first_mass fossilness_fossilness fossilness_most_massive_not_first"
CSV_MAPS="c200c_c=c200c fossilness_first_mass=fossilness_mcent fossilness_fossilness=fossilness fossilness_most_massive_not_first=fossilness_msat"
PARAM="--map $CSV_MAPS  --csv-columns $CSV_COLS"

#(Box0mr_bao_z0 && python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao_1cluster $PARAM)

#(Box0mr_bao_z0 && DB=ciao.sql python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__z0_$PROPS.0 $PARAM)
#exit
#(Box0mr_bao_z0; tmpfile=$(mktemp); cat output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.*>$tmpfile; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile $tmpfile $PARAM && rm $tmpfile)

#(Box0mr_bao_z0 && python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
#(Box2bhr_bao_z0;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
#(Box4uhr_bao_z0; /usr/bin/python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__z0_$PROPS.* $PARAM)

#(Box0mr_bao_z05; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
#(Box0mr_bao_z1; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
#(Box0mr_bao_z15; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
#(Box0mr_bao_z2;   python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)

#(Box2bhr_bao_z05; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
#(Box2bhr_bao_z1;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
#(Box2bhr_bao_z15; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
#(Box2bhr_bao_z2; python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)


#(Box4uhr_bao_z05; /usr/bin/python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__z05_$PROPS.* $PARAM)
#(Box4uhr_bao_z1; /usr/bin/python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__z1_$PROPS.* $PARAM)
#(Box4uhr_bao_z15; /usr/bin/python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__z15_$PROPS.* $PARAM)
#(Box4uhr_bao_z2; /usr/bin/python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__z2_$PROPS.* $PARAM)


