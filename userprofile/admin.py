from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from userprofile.models import UserSetting
# Register your models here.

class UserSettingInline(admin.StackedInline):
    model = UserSetting
    can_delete = False
    verbose_name_plural = "UserSettings"


class UserAdmin(BaseUserAdmin):
    inlines = [UserSettingInline, ]



# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
