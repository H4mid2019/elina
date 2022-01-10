from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer
from .fetcher import fetch_alphavantage
from datetime import datetime
import pytz


class PostViewSet(viewsets.ViewSet):
    def list(self, request):
        rate = ExchangeRate.objects.all()
        serializer = ExchangeRateSerializer(rate, many=True)
        return Response(serializer.data)

    def create(self, request):
        rate, refresh_date = fetch_alphavantage()

        exchange = ExchangeRate(rate=rate, server_refreshed_date=pytz.utc.localize(datetime.fromisoformat(refresh_date)))
        exchange.save()

        return Response({"rate":rate, "refresh_date":refresh_date}, status=status.HTTP_202_ACCEPTED)