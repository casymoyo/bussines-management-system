from . import views
from django.urls import path

app_name = 'vouchers'

urlpatterns = [
    path('addCategory/', views.addCategory, name='addCategory'),
    path("voucherList/", views.vouchersList,  name="voucherList"),
    path("voucherFiles/", views.voucherFiles,  name="voucherFiles"),
    path("populateVouchers/<int:pk>", views.populateVouchers,  name="populateVouchers"),
]
