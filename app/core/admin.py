from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import ugettext as _
from core import models

from django.contrib.gis import admin


class UserAdmin(admin.OSMGeoAdmin, BaseUserAdmin):
    ordering = ['id']
    list_display = ['email', 'name']
    modifiable = False
    fieldsets = (
        (_('Login Details'), {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Location'), {
         'fields': ('address', 'lat', 'lng', 'location_point')}),
        (_('Permissions'), {
         'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )
    readonly_fields = ['lat', 'lng']


admin.site.register(models.User, UserAdmin)
