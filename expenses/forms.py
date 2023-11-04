from expenses.models import Expense
from django.forms import ModelForm

class ExpensesForm(ModelForm):
    class Meta:
        model = Expense
        exclude = ("user",)
