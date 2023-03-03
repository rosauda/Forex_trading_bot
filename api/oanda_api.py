import requests
import os
import pandas as pd
from dateutil import parser
from datetime import datetime as dt

API_KEY = os.environ["api_key"]
ACCOUNT_ID = os.environ["account_id"]
OANDA_URL = "https://api-fxpractice.oanda.com/v3"


class OandaApi:

    def __init__(self):
        self.session = requests.session()
        self.session.headers.update({
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        })

    def make_request(self, url, verb='get', code=200, params=None, data=None, headers=None):
        full_url = f"{OANDA_URL}/{url}"
        try:
            response = None
            if verb == 'get':
                response = self.session.get(full_url, params=params, data=data, headers=headers)
            elif verb == 'post':
                response = self.session.post(full_url, params=params, data=data, headers=headers)
            elif verb == 'put':
                response = self.session.put(full_url, params=params, data=data, headers=headers)
            elif verb == 'delete':
                response = self.session.delete(full_url, params=params, data=data, headers=headers)
            else:
                return False, {'error': 'verb not found'}

            if response.status_code == code:
                return True, response.json()
            else:
                return False, response.json()

        except Exception as error:
            return False, {'Exception': str(error)}

    def get_account_ep(self, ep, data_key):
        url = f"accounts/{ACCOUNT_ID}/{ep}"
        ok, data = self.make_request(url)

        if ok == True and data_key in data:
            return data[data_key]
        else:
            print("ERROR get_account_ep()", data)
            return None

    def get_account_summary(self):
        return self.get_account_ep("summary", "account")

    def get_account_instruments(self):
        return self.get_account_ep("instruments", "instruments")

    def fetch_candles(self, pair_name, count=10, granularity="H1", price='MBA', date_f=None, date_t=None):
        url = f"instruments/{pair_name}/candles"
        params = dict(
            granularity=granularity,
            price=price,
        )

        if date_f is not None and date_t is not None:
            date_format = "%Y-%m-%dT%H:%M:%SZ"
            params["from"] = dt.strftime(date_f, date_format)
            params["to"] = dt.strftime(date_t, date_format)
        else:
            params["count"] = count

        ok, data = self.make_request(url, params=params)
        if ok == True and 'candles' in data:
            return data['candles']
        else:
            print("ERROR fetch_candles()", params, data)
            return None

    def get_candles_df(self, pair_name, **kwargs):

        data = self.fetch_candles(pair_name, **kwargs)

        if data is None:
            return None
        if len(data) == 0:
            return pd.DataFrame()

        # Creating data frame
        prices = ['mid', 'bid', 'ask']
        ohlc = ['o', 'h', 'l', 'c']

        final_data = [{**{'time': parser.parse(candle['time']), 'volume': candle['volume']},
                       **{f"{p}_{o}": float(candle[p][o]) for p in prices if p in candle for o in ohlc}}
                      for candle in data if candle['complete']]
        df = pd.DataFrame.from_records(final_data)

        return df

























