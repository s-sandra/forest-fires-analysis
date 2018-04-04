# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()

# creates dataframe where fire durations are expressed in total minutes. Removes columns where cont_date is null.
# if cont_time is not provided, sets to 2359. if disc_time is not provided, sets to 0000.
fire_durations = pd.read_sql("select fod_id, (cont_date * 24 * 60 + substr(ifnull(cont_time, \"2359\"), 1, 2) * 60 + "
                             "substr(ifnull(cont_time, \"2359\"), 3, 2)) - (discovery_date * 24 * 60 + "
                             "substr(ifnull(discovery_time, \"0000\"), 1, 2) * 60 + substr(ifnull(discovery_time, "
                             "\"0000\"), 3, 2)) fire_duration from fires where cont_date is not null", con)

# some fire acres are placed in classes. Should we ignore those?

# extracts primary key FOD_ID and the unit type (landowner) from the agency that reported the fire.
# value in UnitType column can be US Federal, US State, US County/Local, Tribe or Interagency.
land_owner = pd.read_sql("select fod_id, UnitType  from fires join nwcg_unitidactive_20170109 "
                        "on nwcg_reporting_unit_id==unitid", con)

fire_size = pd.read_sql("select fod_id, fire_size from fires")
fire_year = pd.read_sgl("select fod_id, fire_year from fires")
fire_state = pd.read_sgl("select fod_id, state from fires")
fire_cause = pd.read_sql("select fod_id, stat_cause_descr from fires")