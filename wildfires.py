# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd

con = sqlite3.connect("RDS-2013-0009.4_SQLite/Data/FPA_FOD_20170508.sqlite")
cur = con.cursor()

# Creates DataFrame containing fire size, year, state, cause, duration and landowner. Fire durations are expressed in
# total minutes. Removes columns where cont_date is null. if cont_time is not provided, sets to 2359.
# If disc_time is not provided, sets to 0000.
fires = pd.read_sql("select "
                             "fire_size, " # in acres
                             "fire_year, "
                             "fires.state, " # as abbreviation
                             "(cont_date * 24 * 60 + substr(ifnull(cont_time, \"2359\"), 1, 2) * 60 + "
                             "substr(ifnull(cont_time, \"2359\"), 3, 2)) - (discovery_date * 24 * 60 + "
                             "substr(ifnull(discovery_time, \"0000\"), 1, 2) * 60 + substr(ifnull(discovery_time, "
                             "\"0000\"), 3, 2)) FIRE_DURATION, " 
                             "UnitType,"
                             "stat_cause_descr " # fire cause. Can be US Federal, US State, US County/Local, Tribe or Interagency.
                             "from fires join nwcg_unitidactive_20170109 on nwcg_reporting_unit_id==unitid "
                             "where cont_date is not null", con)