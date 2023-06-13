from django.contrib import admin
from .models import Product,Variation,ProductGallery
import admin_thumbnails

@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    #To prepopulate slug according to product name...
    prepopulated_fields = {'slug':('product_name',)}
    #list_display will display these items in admin panel Product page
    list_display = ('product_name','price','stock','category','modified_date','is_available')
    inlines = [ProductGalleryInline]

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','is_active')
    #changing specific field in admin panel
    list_editable = ('is_active',)
    #adding filterbox as sidebar in admin panel
    list_filter = ('product','variation_category','variation_value')

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ProductGallery)
