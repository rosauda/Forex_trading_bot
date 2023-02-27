import os
import requests
import pandas as pd
import json
from dateutil import parser

# ---------------------------- VARIABLES ------------------------------- #

API_KEY = os.environ["api_key"]
ACCOUNT_ID = os.environ["account_id"]
OANDA_URL = "https://api-fxpractice.oanda.com/v3"
CURRENCIES = ['EUR', 'USD', 'GBP', 'JPY', 'CHF', 'NZD', 'CAD', 'AUD']

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

# List containing the information that I need for each instrument
key_i = ['name', 'type', 'displayName', 'pipLocation', 'displayPrecision', 'tradeUnitsPrecision', 'marginRate']

# Creating a dictionary containing instrument`s information key_i
instruments_dict = {}
for i in instruments_list:
    key = i['name']
    instruments_dict[key] = {k: i[k] for k in key_i}

# Saving data to a json file in the project folder
with open("../data/instrument.json", "w") as f:
    json.dump(instruments_dict, f, indent=2)

# ---------------------------- DEFINING FUNCTIONS ------------------------------- #


def fetch_candles(pair_name, count=10, granularity="H1"):
    url = f"{OANDA_URL}/instruments/{pair_name}/candles"
    params = dict(
        count=count,
        granularity=granularity,
        price="MBA",
    )

    try:
        response = session.get(url, params=params, data=None, headers=None)
        response.raise_for_status()  # Raises an exception for non-2xx response codes
        data = response.json()
        if "candles" in data:
            data = data['candles']
        else:
            data = []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
        data = []

    return response.status_code, data


def get_candles_df(data):
    # Creating data frame
    prices = ['mid', 'bid', 'ask']
    ohlc = ['o', 'h', 'l', 'c']

    if len(data) == 0:
        return pd.DataFrame()

    final_data = [{**{'time': parser.parse(candle['time']), 'volume': candle['volume']},
                   **{f"{p}_{o}": float(candle[p][o]) for p in prices for o in ohlc}}
                  for candle in data if candle['complete']]
    df = pd.DataFrame.from_records(final_data)
    return df


def create_data_file(pair_name, count=10, granularity="H1"):
    code, data = fetch_candles(pair_name, count, granularity)
    if code != 200:
        print("Failed", pair_name, data)
        return
    if len(data) == 0:
        print("No candles", pair_name)
    candles_df = get_candles_df(data)
    candles_df.to_pickle(f"../data/{pair_name}_{granularity}.pkl")
    print(f"{pair_name} {granularity} {candles_df.shape[0]} candles, {candles_df.time.min()} {candles_df.time.max()}")


if __name__ == "__exploration__":
    code, data = fetch_candles("EUR_USD", count=10, granularity="H4")
    candles_df = get_candles_df(data)
    create_data_file("EUR_USD", count=10, granularity="H4")
    # Getting the main pairs
    for p1 in CURRENCIES:
        for p2 in CURRENCIES:
            pr = f"{p1}_{p2}"
            if pr in instruments_dict:
                for g in ['H1', 'H4']:
                    create_data_file(pr, count=4001, granularity="H4")

    print(candles_df.info())

CURRENCIES = ['EUR', 'USD', 'GBP', 'JPY', 'CHF', 'NZD', 'CAD', 'AUD']
for p1 in CURRENCIES:
    for p2 in CURRENCIES:
        pr = f"{p1}_{p2}"
        if pr in instruments_dict:
            for g in ['H1', 'H4']:
                create_data_file(pr, count=4001, granularity=g)