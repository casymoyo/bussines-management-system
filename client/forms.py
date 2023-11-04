from django.forms import ModelForm
from client.models import Client, Cancellation

    
class ClientForm(ModelForm):
    
    class Meta:
        model = Client
        exclude = ("user", "count")

class ClientMememberForm(ModelForm):
    class Meta:
        model = Client
        exclude = ("user", "count")


class ClientDayForm(ModelForm):
    class Meta:
        model = Client
        exclude = ("user", "count", "id_number", "address")


class ClientCancellation(ModelForm):
    class Meta:
        model = Cancellation
        exclude = ("user",)
