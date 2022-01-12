from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from .models import ExchangeRate
from .serializers import ExchangeRateSerializer, UserSerializer
from .fetcher import fetch_alphavantage
from datetime import datetime
import pytz
import logging

logger = logging.getLogger(__name__)


class PostViewSet(viewsets.ViewSet):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def list(self, request):
        """this method retruns the all exchange rates which has been saved from the db
        """
        rates = ExchangeRate.objects.all()
        serializer = ExchangeRateSerializer(rates, many=True)
        return Response(serializer.data)

    def force_fetch(self, request):
        """this methid send the request to the API endpoint and add the date to db also it returns the data.
        """

        rate, refresh_date = fetch_alphavantage()
        if rate:
            exchange = ExchangeRate.objects.create(rate=rate, server_refreshed_date=pytz.utc.localize(
                datetime.fromisoformat(refresh_date)))
            serializer = ExchangeRateSerializer(exchange)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        logger.warning("I couldn't fetch the API endpoint")
        return Response({"error": "I couldn't fetch the API endpoint", "rate": None},
                        status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def retrieve(self, request, pk=None):
        """this method returns only the latest exchange rate from db
        """
        rate = ExchangeRate.objects.last()
        serializer = ExchangeRateSerializer(rate)
        return Response(serializer.data)


@api_view(['POST'])
def create_auth(request):
    """this view function creates a user in django db so then the user can obtain a token
    """
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid(raise_exception=True):
        serialized.save()
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_api_key(request):
    """this view function accepts only post requests and a json with name then creates api_key and retruns them, 
    if name doesn't provide by defult uses unknown

    """
    api_key_instance, key = APIKey.objects.create_key(name=request.data.get("name", "unknown"))
    return Response({"key": key, "name": api_key_instance.name}, status=status.HTTP_201_CREATED)
