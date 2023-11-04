from django.urls import path
from . import views

app_name = 'transactions'
urlpatterns = [
    path("create/", views.TransactioinCreateView, name="create"),
    path('account/<int:pk>', views.Account, name='account'),
    path('pdf/<int:pk>', views.clientAccountPdfGenerator, name='clientAccount'),
    path('transactions/', views.transactions, name='transactions'),
    path('dailyReport/', views.dailyReport,  name='dailyReport'),
    # path('customReport/', views.customReport,  name='customReport'),
    path('monthlyReport/', views.monthlyReport,  name='monthlyReport'),
]
