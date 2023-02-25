import os
import requests
import pandas as pd
import json

# ---------------------------- VARIABLES ------------------------------- #

API_KEY = os.environ["api_key"]
ACCOUNT_ID = os.environ["account_id"]

oanda_url = "https://api-fxpractice.oanda.com/v3"

# ---------------------------- VARIABLES ------------------------------- #

# Creating a session object
session = requests.Session()







