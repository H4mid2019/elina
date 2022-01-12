from sys import flags
import requests
import os

API_KEY = os.getenv('ALPHAVANTAGE_API_TOKEN', "demo")


def fetch_alphavantage():
    """fetches the alphavantage url and gets the response and returns exchange rate and last refreshed

    Returns:
        tuple: exchange rate, last refreshed in success case otherwise it returns false,false
    """
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={API_KEY}'
    r = requests.get(url)
    if r.status_code == 200:
        data = r.json().get("Realtime Currency Exchange Rate")
        return data.get("5. Exchange Rate"), data.get("6. Last Refreshed")
    else:
        return False, False
