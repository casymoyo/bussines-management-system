from . import views
from django.urls import path
from django.views.generic import TemplateView

app_name = "client"
urlpatterns = [
    path("", views.ClientsListView, name="clients"),
    path("clientDetail/<int:pk>", views.ClientsDetailView, name="detail"),
    path("createClient/", views.ClientCreateView, name="createClient"),
    path("createPermanent/", views.PermanentCreateView, name='createPermanent'),
    path(
        "clientCancellatioin/<int:pk>",
        views.ClientCancellation,
        name="clientCancellation",
    ),
    
    path("updatePermanent/<int:pk>", views.UpdateNonPermenent, name='updatePermanent'),
    path("updateNonPermanent/<int:pk>", views.UpdateNonPermenent, name='updateNonPermanent'),
    
    # pdf 
    path("clientsPdf/", views.clientPdfGenerator, name="clientsPdf"),
    
    # Pos url
    path("pos/", views.Pos, name="pos"),
    path('posData/', views.posData, name='posData'),
]
