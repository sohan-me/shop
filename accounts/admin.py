from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, UserProfile
from django.utils.html import format_html
# Register your models here.


class AccountAdminView(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name', 'username')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class AdminUserProfile(admin.ModelAdmin):
    
    def thumbnail(self, object):
        try:
            return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_image.url))
        except:
            pass    
        thumbnail.shore_description = 'Profile Picture'
        list_display = ['thumbnail', 'user', 'address_line_1', 'address_line_2', 'city', 'state', 'country']


admin.site.register(Account, AccountAdminView)
admin.site.register(UserProfile, AdminUserProfile)