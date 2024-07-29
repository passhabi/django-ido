from django.db import models
from django.contrib.auth.models import User
from collections import namedtuple

PRIORITY_CHOICES = {
    1: 'Important and Urgent',
    2: 'Important',
    3: 'Urgent',
    4: 'Not Urgent, Important',
}


# Create your models here.
class Todolist(models.Model):
    title = models.CharField(null=False, blank=False, max_length=300)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.SmallIntegerField(blank=True, null=True, choices=PRIORITY_CHOICES)
    category = models.IntegerField(blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return self.title


class UserSetting(models.Model):
    ORDER_BY_CHOICES = {'d': 'due_date', 't': 'title', 'c': 'creation_date'}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_by = models.CharField(null=False, blank=False, max_length=1, default='d',
                                choices=ORDER_BY_CHOICES)
    is_descending = models.BooleanField(default=True, blank=False, null=False)

    image_profile = models.ImageField(null=True, blank=True, upload_to='image/profiles/')

    def __str__(self) -> str:
        return "Todo list view"
