# @ authors Hannah Frederick, Sandra Shtabnaya and Jorge Contreras

import sqlite3
import pandas as pd
import scipy.stats

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
                             "\"0000\"), 3, 2)) FIRE_DURATION, " # in minutes
                             "UnitType," # entity that owns the land where the fires occurred.
                             "stat_cause_descr " # fire cause. Can be US Federal, US State, US County/Local, Tribe or Interagency.
                             "from fires join nwcg_unitidactive_20170109 on nwcg_reporting_unit_id==unitid "
                             "where cont_date is not null", con)

# changes column names.
fires.columns = ["size", "year", "state", "duration", "landowner", "cause"]

probs = {} # dictionary containing prior and conditional probabilities for categorical features.
densities = {} # dictionary containing density values for numerical features.

labels = fires.cause.drop_duplicates()
numeric_features = ["duration", "size", "year"]
categorical_features = ["state", "landowner"]

training_data = fires.sample(frac=0.7) # 70% of data used for training
test_data = fires.drop(training_data.index) # the remaining 30% is used for testing classifier

for label in labels:
    # get all the rows in training data with the current label. Store it in a variable called rows.
    rows = None
    # add a key-value pair to probs, where the key is the label and the value is the prior probability of the label.

    # computes densities for all numeric features given the current label.
    for feature in numeric_features:
        density = scipy.stats.norm(rows.feature.mean(), rows.feature.std())
        densities[feature + "|" + label] = density

    # computes conditional probs for all categorical features given the current label.
    for feature in categorical_features:
        probs[feature + "|" + label] = None
        # loop through all the possible values for each categorical feature
        # for each value, calculate the probability of both the value and the label together.
        # store the result as a key-value pair in probs, where the key is "feature|label" and the value
        # is the probability.

# documentation goes here.
def predict(size, year, state, duration, landowner, cause):
    scores = [] # stores the probability of inputted features given each label.
    highest_prob = 0
    prediction = ""

    # computes probability of all features given each label.
    for label in labels:
        # obtain and store the prior probability of the current label in a variable called prob.
        prob = 0

        prob *= densities["size|" + label].pdf(size)
        prob *= densities["year|" + label].pdf(year)
        prob *= densities["duration|" + label].pdf(duration)

        # obtain conditional probability for landowner given label from probs, multiply by prob and set product equal to prob.
        # obtain conditional probability for state given label from probs, multiply by prob and set product equal to prob.

        # check if the current prob is greater than highest_prob. If yes, set highest_prob to prob and prediction
        # to current label.

        scores.append(prob)

    return [prediction, highest_prob / sum(scores)]

