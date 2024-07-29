from django.forms import ModelForm
from todos.models import Todolist

class TodolistForm(ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'description', 'due_date', 'priority', 'category']