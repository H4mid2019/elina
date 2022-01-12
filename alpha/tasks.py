from celery import shared_task
from .models import ExchangeRate
from .fetcher import fetch_alphavantage
from datetime import datetime
import pytz

@shared_task
def scheduled_fetcher():
    """it's a tsk function of celery which scheduled ro run every hour

    Returns:
        string: a word as success
    """
    # fetches the alphavantage api to get 
    rate, refresh_date = fetch_alphavantage()
    # it saves the data into db 
    if rate:
        exchange = ExchangeRate(rate=rate, server_refreshed_date=pytz.utc.localize(datetime.fromisoformat(refresh_date)))
        exchange.save()
        return "success"
    return "error in retrieving data"
