from django.contrib import admin
from vouchers.models import *

admin.site.register(vouchers)
admin.site.register(voucherFile)
admin.site.register(voucherTransaction)
admin.site.register(voucherCategory)

