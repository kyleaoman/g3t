set -ev
. sims.bash
db_1e4_ago

python subfind_to_sql.py || true

#DB=/tmp/antonio/magneticum.sql.1e4.to
PROPS="c200c_fossilness"
CSV_COLS="c200c_c c200c_rho0 c200c_rs fossilness_first_mass fossilness_fossilness fossilness_most_massive_not_first"
CSV_MAPS="c200c_c=c200c fossilness_first_mass=fossilness_mcent fossilness_fossilness=fossilness fossilness_most_massive_not_first=fossilness_msat"
#CSV_COLS="c200c_c"
PARAM="--map $CSV_MAPS  --csv-columns $CSV_COLS"


(Box0mr_bao_z0 &&   python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
(Box2bhr_bao_z0 &&   python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
(Box4uhr_bao_z0 &&  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__${TAG}_$PROPS.* $PARAM)

(Box0mr_bao_z05;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
(Box0mr_bao_z1;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
(Box0mr_bao_z15;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)
(Box0mr_bao_z2;    python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box0_mr_bao__${TAG}_$PROPS.* $PARAM)

(Box2bhr_bao_z05;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
(Box2bhr_bao_z1;   python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
(Box2bhr_bao_z15;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)
(Box2bhr_bao_z2;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box2b_hr_bao__${TAG}_$PROPS.* $PARAM)


(Box4uhr_bao_z05;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__${TAG}_$PROPS.* $PARAM)
(Box4uhr_bao_z1;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__${TAG}_$PROPS.* $PARAM)
(Box4uhr_bao_z15;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__${TAG}_$PROPS.* $PARAM)
(Box4uhr_bao_z2;  python csv_to_sql.py --simulation-name $NAME --snap $SNAP --outfile output/_HydroSims_Magneticum_Box4_uhr_test__${TAG}_$PROPS.* $PARAM)


