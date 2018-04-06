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

# consider calculating fire duration using cont_doy and discovery_doy.

probs = {} # dictionary containing prior and conditional probabilities for categorical features.
densities = {} # dictionary containing density values for numerical features.

labels = fires.cause.drop_duplicates()
numeric_features = ["duration", "size", "year"]
categorical_features = ["state", "landowner"]

training_data = fires.sample(frac=0.7) # 70% of data used for training
test_data = fires.drop(training_data.index) # the remaining 30% is used for testing classifier

for label in labels:
    rows = training_data[training_data.cause == label]
    probs[label] = len(rows) / len(training_data) # calculates the prior probability for each label value.

    # computes densities for all numeric features given the current label.
    for feature in numeric_features:
        density = scipy.stats.norm(rows[feature].mean(), rows[feature].std())
        densities[feature + "|" + label] = density

    # computes conditional probs for all categorical features given the current label.
    for feature in categorical_features:
        for value in training_data[feature].drop_duplicates(): # loops through all the possible values for each categorical feature.
            probs[value + "|" + label] = len(rows[rows[feature] == value]) / len(rows) # the probability of both the value and the label together.

    print("Computed probabilities for label value " + label + " in training data....")

print(densities)
# documentation goes here.
def predict(size, year, state, duration, landowner):
    scores = [] # stores the probability of inputted features given each label.
    highest_prob = 0
    prediction = ""

    # computes probability of all features given each label.
    for label in labels:
        prob = probs[label] # obtains the prior probability of the current label.

        prob *= densities["size|" + label].pdf(size)
        prob *= densities["year|" + label].pdf(year)
        prob *= densities["duration|" + label].pdf(duration)

        prob *= probs[state + "|" + label]
        prob *= probs[landowner + "|" + label]

        # checks if the current prob is greater than highest_prob.
        # If so, updates prediction and highest_prob.
        if prob > highest_prob:
            highest_prob = prob
            prediction = label

        scores.append(prob)

    return [prediction, highest_prob / sum(scores)]

num_correct = 0

# iterates through all rows of test data
for i in range(len(test_data)):
    row = test_data.iloc[i]
    prediction, confidence = predict(row.size, row.year, row.state, row.duration, row.landowner)

    # checks if outputted prediction matches test label.
    if prediction == row.cause:
        num_correct += 1

    print("Computed row " + str(i) + " in test data. Predicted: " + prediction + ". Confidence: " + str(confidence))

print("We got " + str(num_correct / len(test_data) * 100) + "% correct on the test data.")
# We got 30.83885626445345% correct on the test data.