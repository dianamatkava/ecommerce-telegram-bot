import os
import requests
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('COINGATE_RATE_API', None)


def get_fiat_amount(currency, coin, price):
    headers = {"accept": "text/plain"}
    response = requests.get(
        '/'.join([URL, currency, coin]), 
        headers=headers
    )
    if response.status_code == 200:
        return round(float(response.text) * price, 8)
    