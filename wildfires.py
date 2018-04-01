# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()
fire_durations = pd.read_sql("select DISCOVERY_DATE,DISCOVERY_DOY,DISCOVERY_TIME,CONT_DATE,CONT_DOY,CONT_TIME from fires limit 20", con)
epoch = pd.to_datetime(0, unit="s").to_julian_date() # start of epoch on the Julian Calendar

# discovery date and contained date is in Julian days, converts to dates.
fire_durations.DISCOVERY_DATE = pd.to_datetime(fire_durations.DISCOVERY_DATE - epoch, unit="D")
fire_durations.CONT_DATE = pd.to_datetime(fire_durations.CONT_DATE - epoch, unit="D")
print(fire_durations)