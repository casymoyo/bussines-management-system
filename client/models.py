from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=50)
    phonenumber = models.CharField(max_length=50)
    member_status = models.CharField(max_length=50)
    user = models.ForeignKey("user.User", on_delete=models.CASCADE)
    count = models.IntegerField()

    def __str__(self):
        return self.name

class Account(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    transaction = models.ForeignKey("transactions.Transactions", on_delete=models.CASCADE)

    def __str__(self):
        return self.client.name
     

    
