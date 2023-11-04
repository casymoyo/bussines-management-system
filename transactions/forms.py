from client.models import Client
from transactions.models import Transaction
from django import forms


class TransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        exclude = ("user", 'owing', 'date_due', 'status')
      