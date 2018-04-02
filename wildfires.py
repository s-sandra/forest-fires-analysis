# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()

# creates dataframe where fire durations are expressed in total minutes.
fire_durations = pd.read_sql("select cont_date * 24 * 60 + substr(cont_time, 1, 2) * 60 + "
                             "substr(cont_time, 3, 2) - discovery_date * 24 * 60 + substr(discovery_time, 1, 2) * 60 + "
                             "substr(discovery_time, 3, 2) duration from fires", con)

# epoch = pd.to_datetime(0, unit="s").to_julian_date() # start of epoch on the Julian Calendar

# discovery date and contained date is in Julian days (as float), converts to timestamp.
# fire_durations.DISCOVERY_DATE = pd.to_datetime(fire_durations.DISCOVERY_DATE - epoch, unit="D")
# fire_durations.CONT_DATE = pd.to_datetime(fire_durations.CONT_DATE - epoch, unit="D")

# what if time is none, but date appears?
# some fire acres are placed in classes. Should we ignore those
fire_durations = fire_durations.dropna()
land_owner = pd.read_sql("select UnitType from NWCG_UnitIDActive_20170109 limit 20", con)
print(land_owner)