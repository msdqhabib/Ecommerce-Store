from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    #To prepopulate slug according to product name...
    prepopulated_fields = {'slug':('product_name',)}
    #list_display will display these items in admin panel Product page
    list_display = ('product_name','price','stock','category','modified_date','is_available')
admin.site.register(Product, ProductAdmin)
