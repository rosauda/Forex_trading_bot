import requests
import os

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


