# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()

# creates dataframe where fire durations are expressed in total minutes.
fire_durations = pd.read_sql("select fod_id, cont_date * 24 * 60 + substr(cont_time, 1, 2) * 60 + "
                             "substr(cont_time, 3, 2) - discovery_date * 24 * 60 + substr(discovery_time, 1, 2) * 60 + "
                             "substr(discovery_time, 3, 2) fire_duration from fires", con)

# what if time is none, but date appears?
# some fire acres are placed in classes. Should we ignore those?

# extracts primary key FOD_ID and the unit type (landowner) from the agency that reported the fire.
# value in UnitType column can be US Federal, US State, US County/Local, Tribe or Interagency.
land_owner = pd.read_sql("select fod_id, UnitType  from fires join nwcg_unitidactive_20170109 "
                        "on nwcg_reporting_unit_id==unitid", con)