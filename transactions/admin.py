from django.contrib import admin
from transactions.models import *

admin.site.register(Product)
admin.site.register(Transaction)
admin.site.register(TransactionLog)
