from django.contrib import admin
from todos.models import Todolist

class TodolistAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', ]

# Register your models here.
admin.site.register(Todolist, TodolistAdmin)

