from django.contrib import admin
from .models import Account,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

class AccountAdmin(UserAdmin):
    list_display = ['email','first_name','last_name','username','last_login','date_joined','is_active']
    #display_links will make these field clickable link
    list_display_links = ('email','first_name','last_name')
    #readoinly fields will only be readable
    readonly_fields = ('last_login','date_joined')
    #-ive makes ordering of accounts will be in descending order
    ordering = ('-date_joined',)

    filter_horizontal =()
    list_filter =()
    #fieldset will make password read only
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self,object):
        return format_html('<img src="{}" width= "30" style="border-radius:50%";>'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail','user','city','state','country')

admin.site.register(Account,AccountAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
