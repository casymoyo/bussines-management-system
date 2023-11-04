from django.urls import path
from dashboard.views import Dashboard

app_name = "dashboard"
urlpatterns = [path("", Dashboard, name="dashboard")]
