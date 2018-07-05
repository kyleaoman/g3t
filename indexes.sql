CREATE UNIQUE INDEX "simulation_name" ON "simulation" ("name");


CREATE INDEX "snap_simulation_id" ON "snap" ("simulation_id");
CREATE INDEX "foffile_snap_id" ON "foffile" ("snap_id");
CREATE INDEX "galaxy_snap_id" ON "galaxy" ("snap_id");

CREATE INDEX galaxy_i  ON galaxy (snap_id,id_cluster);

CREATE INDEX galaxy_i_pos  ON galaxy (snap_id,id_cluster,spos0,spos1,spos2);

CREATE INDEX "fof_snap_id" ON "fof" ("snap_id");
CREATE INDEX "pp_snap_id" ON "pp" ("snap_id");

CREATE UNIQUE INDEX "fof_snap_cluster_id" ON "fof" ("snap_id", "id_cluster");
CREATE UNIQUE INDEX "pp_snap_cluster_id" ON "pp" ("snap_id", "id_cluster");
