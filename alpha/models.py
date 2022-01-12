from django.db import models


class ExchangeRate(models.Model):
    class Meta:
        verbose_name = "Exchange Rate BTC/USD"
        verbose_name_plural = "Exchange Rates BTC/USD"

    rate = models.DecimalField(max_digits=20, decimal_places=6)
    fetch_date = models.DateTimeField(auto_now_add=True, blank=True)
    server_refreshed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"fetched hour: {self.fetch_date.hour}"
