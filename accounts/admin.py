from django.contrib import admin
from django.contrib.auth.models import Group

from accounts.models.users import AMSUser, AMSGroup


admin.site.unregister(Group)

@admin.register(AMSUser)
class AMSUserAdmin(admin.ModelAdmin):
    list_display = 'id', 'full_name', 'email'


@admin.register(AMSGroup)
class AMSGroupAdmin(admin.ModelAdmin):
    pass