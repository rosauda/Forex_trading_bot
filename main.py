import os
import requests
import pandas as pd
import json

# ---------------------------- VARIABLES ------------------------------- #

API_KEY = os.environ["api_key"]
ACCOUNT_ID = os.environ["account_id"]
OANDA_URL = "https://api-fxpractice.oanda.com/v3"

# ---------------------------- TESTING API ------------------------------- #

# Creating a session object
session = requests.Session()

session.headers.update({
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
})

# Defining parameters
params = dict(
    count=10,
    granularity="H1",
    price="MBA",
)

# Generating url
url = f"{OANDA_URL}/accounts/{ACCOUNT_ID}/instruments"

# ---------------------------- GETTING DATA FROM OANDA ------------------------------- #

# Making request
response = session.get(url, params=None, data=None, headers=None)
data = response.json()

# Creating a list with all instruments
instruments_list = data["instruments"]
print(instruments_list[0].keys())

# List containing the information that I need for each instrument
key_i = ['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision', 'marginRate']

# Creating a dictionary containing instrument`s information key_i
instruments_dict = {}
for i in instruments_list:
    key = i['name']
    instruments_dict[key] = {k: i[k] for k in key_i}

# Saving data to a json file in the project folder
with open("instrument.json", "w") as f:
    f.write(json.dumps(instruments_dict, indent=2))
