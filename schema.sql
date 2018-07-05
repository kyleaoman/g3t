CREATE TABLE "simulation" ("id" INTEGER NOT NULL PRIMARY KEY, "name" TEXT NOT NULL, "box_size" REAL, "h" REAL);

CREATE UNIQUE INDEX "simulation_name" ON "simulation" ("name");

CREATE TABLE "snap" ("id" INTEGER NOT NULL PRIMARY KEY, "name" TEXT, "redshift" REAL, "a" REAL, "simulation_id" INTEGER NOT NULL, "tag" TEXT, FOREIGN KEY ("simulation_id") REFERENCES "simulation" ("id"));

CREATE INDEX "snap_simulation_id" ON "snap" ("simulation_id");

CREATE TABLE "fof" (
       "id" INTEGER NOT NULL, 
       "id_cluster" INTEGER NOT NULL,
       "snap_id" INTEGER NOT NULL,
       "i_file" INTEGER NOT NULL, "i_in_file" INTEGER NOT NULL, "resolvness" INTEGER NOT NULL, "fsub" REAL, "ncon" REAL, "gpos0" REAL, "gpos1" REAL, "gpos2" REAL, "goff" REAL, "lgas0" REAL, "lgas1" REAL, "lgas2" REAL, "lgas3" REAL, "lgas4" REAL, "lgas5" REAL, "ygas0" REAL, "ygas1" REAL, "ygas2" REAL, "ygas3" REAL, "ygas4" REAL, "ygas5" REAL, "tgas0" REAL, "tgas1" REAL, "tgas2" REAL, "tgas3" REAL, "tgas4" REAL, "tgas5" REAL, "mstr0" REAL, "mstr1" REAL, "mstr2" REAL, "mstr3" REAL, "mstr4" REAL, "mstr5" REAL, "start_subfind_file" INTEGER, "end_subfind_file" INTEGER, "mtop" REAL, "rtop" REAL, "mmea" REAL, "rmea" REAL, "rcri" REAL, "m200" REAL, "r200" REAL, "mcon" REAL, "rcon" REAL, "m500" REAL, "r500" REAL, "m5cc" REAL, "r5cc" REAL, "mtot" REAL, "rtot" REAL, "mvir" REAL, "rvir" REAL, "m25k" REAL, "r25k" REAL, "glen" INTEGER, "nsub" INTEGER, "bgpo0" REAL, "bgpo1" REAL, "bgpo2" REAL, "bgma" REAL, "mgas0" REAL, "mgas1" REAL, "mgas2" REAL, "mgas3" REAL, "mgas4" REAL, "mgas5" REAL, "mgas6" REAL, "bgra" REAL, "mcri" REAL,

       FOREIGN KEY ("snap_id") REFERENCES "snap" ("id"),
       PRIMARY KEY ("snap_id","id_cluster")


) WITHOUT ROWID;

CREATE TABLE "pp" (
       "id" INTEGER NOT NULL,
       "snap_id" INTEGER NOT NULL,
       "id_cluster" INTEGER NOT NULL,
	 "c200c" REAL, "c200c_rho0" REAL, "c200c_rs" REAL, "fossilness_mcent" REAL, "fossilness_msat" REAL, "fossilness" REAL, "virialness_w" REAL, "virialness_es" REAL, "virialness_k" REAL, "virialness_w_gas" REAL, "virialness_es_gas" REAL, "virialness_k_gas" REAL, "virialness_eta" REAL, "virialness_beta" REAL, 


       FOREIGN KEY ("snap_id") REFERENCES "snap" ("id"),
       PRIMARY KEY ("snap_id","id_cluster")
) WITHOUT ROWID;

CREATE TABLE "foffile" (
       "id" INTEGER NOT NULL,
       "ifile" INTEGER NOT NULL,
       "snap_id" INTEGER NOT NULL,
       "id_first_cluster" INTEGER NOT NULL,
       FOREIGN KEY ("snap_id") REFERENCES "snap" ("id"),
       PRIMARY KEY ("snap_id","ifile")


) WITHOUT ROWID;

CREATE TABLE "galaxy" (
       "id" INTEGER NOT NULL,
       "snap_id" INTEGER NOT NULL,
       "id_cluster" INTEGER NOT NULL,
       "spos0" REAL, "spos1" REAL, "spos2" REAL,
       "i_file" INTEGER NOT NULL, "slen" REAL, "grnr" INTEGER NOT NULL, "sage" REAL, "ssfr" REAL, "vmax" REAL, "dust10" REAL, "dsub" REAL, "dust1" REAL, "dust0" REAL, "dust3" REAL, "dust2" REAL, "dust5" REAL, "dust4" REAL, "dust7" REAL, "dust6" REAL, "dust9" REAL, "smst2" REAL, "smst3" REAL, "rhms" REAL, "svel0" REAL, "spin1" REAL, "spin0" REAL, "sz" REAL, "ssub" REAL, "svel1" REAL, "scm2" REAL, "svel2" REAL, "rmax" REAL, "scm0" REAL, "scm1" REAL, "smst4" REAL, "smst5" REAL, "msub" REAL, "smst0" REAL, "smst1" REAL, "soff" REAL, "smhi" REAL, "mbid" REAL, "dust8" REAL, "spin2" REAL,

       FOREIGN KEY ("snap_id") REFERENCES "snap" ("id"),
       PRIMARY KEY ("snap_id","id_cluster","spos0", "spos1", "spos2")

) WITHOUT ROWID;


