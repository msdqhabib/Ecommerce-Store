from django.contrib import admin
from .models import Payment,OrderProduct,Order

admin.site.register(Payment)
admin.site.register(Order)
admin.site.register(OrderProduct)
