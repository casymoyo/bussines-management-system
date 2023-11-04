from django.db import models
from djmoney.models.fields import MoneyField


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")

    def __str__(self):
        return self.name


class Transaction(models.Model):
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    owing = MoneyField(
        max_digits=14, decimal_places=2, default_currency="USD", default=0,
        blank = True
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    work_station = models.ForeignKey("client.WorkStation", on_delete=models.CASCADE, blank=True, null=True)
    # note = models.TextField(blank=True) 
    date_created = models.DateField(auto_now_add=True)
    date_updated = models.DateField(auto_now=True)
    date_due = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=10, default='')

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.client.name} ({self.product.name})"


class TransactionLog(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    action = models.CharField(max_length=50)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return f"{self.date_created} ({self.user.username})"
