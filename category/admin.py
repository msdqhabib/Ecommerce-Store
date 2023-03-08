from django.contrib import admin
from .models import Category
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    #To prepopulate slug according to category name...
    prepopulated_fields = {'slug':('category_name',)}
    #list_display will display these items in admin panel Category page 
    list_display = ('category_name','slug')
admin.site.register(Category,CategoryAdmin)