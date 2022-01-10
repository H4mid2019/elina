import requests
import os


API_KEY = os.getenv('KEY_THAT_MIGHT_EXIST', "demo")



def fetch_alphavantage():
    url = 'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey={API_KEY}'
    r = requests.get(url)
    data = r.json().get("Realtime Currency Exchange Rate")
    return data.get("5. Exchange Rate"),data.get("6. Last Refreshed")