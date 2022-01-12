from django.test import TestCase
from rest_framework.test import APIClient
from django.urls import reverse
from .models import ExchangeRate
from rest_framework_api_key.models import APIKey
from datetime import datetime
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
import pytz


class ExchangeRateTest(TestCase):
    sample_user = "foo"
    sample_password = "foo+secretpass"
    token_key = ""
    api_client = APIClient()

    def setUp(self):
        # Create exchange rates.
        for i in range(45000, 45010):
            refresh_date = datetime.now().isoformat(" ").split(".")[0]
            ExchangeRate.objects.create(rate=f'{i:.6f}', server_refreshed_date=pytz.utc.localize(
                datetime.fromisoformat(refresh_date)))
        _, key = APIKey.objects.create_key(name="test")
        self.api_client.credentials(HTTP_AUTHORIZATION='Api-Key ' + key)
        #  initiate a test user for obtaining a token
        User = get_user_model()
        user = User(email="test@test.com", username="test")
        user.set_password("secret_test")
        user.save()
        token = Token.objects.create(user=user)
        self.token_key = token.key

    def test_exchangerates_count(self):
        rates = ExchangeRate.objects.all()
        self.assertEqual(rates.count(), 10)

    def test_api_key_maker(self):
        response = self.api_client.post("/api/v1/create_api_key", content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertTrue(response.data.get("key"))

    def test_create_user(self):
        response = self.api_client.post(reverse("create_user"),
                                        {"username": self.sample_user, "password": self.sample_password,
                                         "email": "foo@bar.com"}, format="json")
        self.assertEqual(response.status_code, 201)
        response = self.api_client.post(reverse("get_auth_token"),
                                        {"username": self.sample_user, "password": self.sample_password}, format="json")
        self.token = response.data.get("token")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data.get("token", False))

    def test_get_quotes(self):
        response = self.api_client.get("/api/v1/quotes", format="json", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['rate'], '45000.000000')

    def test_force_reload(self):
        response = self.api_client.post("/api/v1/quotes", format="json", content_type="application/json")
        count = ExchangeRate.objects.count()
        self.assertEqual(response.status_code, 202)
        self.assertEqual(count, 11)

    def test_latest_quote(self):
        response = self.api_client.get("/api/v1/quotes", format="json", content_type="application/json")
        self.assertEqual(response.status_code, 200)

    def test_get_quotes_token(self):
        """tests get quotes with token"""
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_key)
        response = self.api_client.get("/api/v1/quotes", format="json", content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['rate'], '45000.000000')

    def test_force_reload_token(self):
        """tests get quotes with token"""
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_key)
        response = self.api_client.post("/api/v1/quotes", format="json", content_type="application/json")
        count = ExchangeRate.objects.count()
        self.assertEqual(response.status_code, 202)
        self.assertEqual(count, 11)