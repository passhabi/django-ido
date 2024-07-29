from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from todos.models import Todolist, UserSetting
from django.contrib.auth.models import User


class TodolistAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', ]


class UserSettingInline(admin.StackedInline):
    model = UserSetting
    can_delete = False
    verbose_name_plural = "UserSettings"


class UserAdmin(BaseUserAdmin):
    inlines = [UserSettingInline, ]




# Register your models here.
admin.site.register(Todolist, TodolistAdmin)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
