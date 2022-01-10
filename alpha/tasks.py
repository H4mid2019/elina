from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task()
def scheduledTask():
    #Get Subscriptions
    print("ttttt")

def on_raw_message(body):
    print(body)
