from django.db import models
from djmoney.models.fields import MoneyField

class Expense(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency="USD")
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.name} ({self.amount})'
    
class ExpenseCancellation(models.Model):
    expense = models.OneToOneField(Expense, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, blank=True)
    date_created = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return f'{self.reason} ({self.expense})'
    
    
    