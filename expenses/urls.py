from expenses.views import Expenses, ExpenseCancellation, dailyReport, monthlyReport, customReport
from django.urls import path

app_name = 'expenses'
urlpatterns = [
    path('', Expenses, name='expenses' ),
    path('dailyReport/', dailyReport,  name='dailyReport'),
    path('customReport/', customReport,  name='customReport'),
    path('monthlyReport/', monthlyReport,  name='monthlyReport'),
    path('cancelExpense/<int:pk>', ExpenseCancellation, name='cancelExpense'),
]
