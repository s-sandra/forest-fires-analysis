# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("my_local_file")
wildfires = pd.read_sql("select FIRE_SIZE from table_name", con)