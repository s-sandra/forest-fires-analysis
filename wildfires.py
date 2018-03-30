# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()
table_names = cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print(table_names.fetchall())
wildfires = pd.read_sql("select * from fires limit 5", con)
print(wildfires)