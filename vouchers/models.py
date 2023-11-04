from django.db import models
from django.utils.translation import gettext_lazy as _

class voucherCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class voucherFile(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='vouchers', max_length=100)
    category = models.ForeignKey("vouchers.voucherCategory", on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50, default='not populated')

    def __str__(self):
        return self.name

class vouchers(models.Model):
    voucher_no = models.CharField(max_length=50)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    file = models.ForeignKey("vouchers.voucherFile", on_delete=models.CASCADE)
    date_created = models.DateField(auto_now_add=True)
    date_used = models.DateField(auto_now=True)
    status = models.CharField(max_length=50, default='unused')

    def __str__(self):
        return self.voucher_no

    
class voucherTransaction(models.Model):
    vouch = models.OneToOneField(vouchers, on_delete=models.CASCADE)
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)
    client = models.ForeignKey("client.Client", on_delete=models.CASCADE)
    work_station = models.ForeignKey("client.WorkStation", on_delete=models.CASCADE, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    start_time = models.TimeField()
    end_time =  models.TimeField()

    def __str__(self):
        return f'{self.client}'










