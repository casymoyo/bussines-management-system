from django.forms import ModelForm
from vouchers.models import voucherFile, vouchers, voucherCategory

class addVoucherFileForm(ModelForm):
    class Meta:
        model = voucherFile
        fields = ('name', 'file', 'category')

class categoryForm(ModelForm):
    class Meta:
        model = voucherCategory
        fields = '__all__'





