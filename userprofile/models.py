from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserSetting(models.Model):
    ORDER_BY_CHOICES = {'d': 'due_date', 't': 'title', 'c': 'creation_date'}

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    order_by = models.CharField(null=False, blank=False, max_length=1, default='d',
                                choices=ORDER_BY_CHOICES)
    is_descending = models.BooleanField(default=True, blank=False, null=False)

    image_profile = models.ImageField(null=True, blank=True, upload_to='image/profiles/')

    def __str__(self) -> str:
        return "Todo list view"
