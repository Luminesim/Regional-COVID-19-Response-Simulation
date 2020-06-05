import pandas as pd

"""
Processes results.
"""

pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
df = pd.read_csv("../../../local/results-20200530T1343.csv")
mapping = {
    'Current Interventions Continue': 1,
    'Current Interventions but Return Schools': 2,
    'Current Interventions but Remove Handwashing, Sanitization, and Social Distancing': 3,
    'No Interventions': 4,
    'Current Interventions but Return Non-Essential Businesses and Going Out': 5,
    'Current Interventions but Return Non-Essential Businesses and Going Out AND Add Masks': 6,
    'Current Interventions but Return Schools, Non-Essential Businesses, and Going Out': 7,
    'Current Interventions but Return Schools, Non-Essential Businesses, and Going Out AND Add Masks': 8,
    'Current Interventions but Add Masks': 9
}
all_result = df.groupby(['experimentId'], as_index=False).agg({'cumulativeInfections': ['mean', 'std']})
all_result = all_result.replace({'experimentId': mapping})
print(all_result)

symp_result = df.groupby(['experimentId'], as_index=False).agg({'cumulativeSymptomatic': ['mean', 'std']})
symp_result = symp_result.replace({'experimentId': mapping})
print(symp_result)
