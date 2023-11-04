from django.db import models

# from phonenumber_field.modelfields import PhoneNumberField

member_status = (("non permanent", "non permanent"), ("permanent", "Permanent"))
station_status = (('occupied', 'occupied'), ('vaccant', 'vaccant'))

class WorkStation(models.Model):
    station = models.CharField(max_length=4)
    type = models.CharField(max_length=10)
    status = models.CharField(max_length=50, choices=station_status)

    def __str__(self) -> str:
        return f'{self.station} ({self.status})'
    
class Client(models.Model):
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True, blank=True)
    id_number = models.CharField(max_length=50, null=True, blank=True)
    station_number = models.OneToOneField(WorkStation, on_delete=models.CASCADE, null=True, blank=True)
    member_status = models.CharField(choices=member_status, max_length=50)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    count = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return self.name


class Cancellation(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    note = models.TextField()

    def __str__(self):
        return self.client.name


class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction = models.ForeignKey(
        "transactions.Transaction", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.client.name} ({self.status})"


    