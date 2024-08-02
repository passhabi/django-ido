# Generated by Django 5.0.6 on 2024-08-02 19:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_by', models.CharField(choices=[('d', 'due_date'), ('t', 'title'), ('c', 'creation_date')], default='d', max_length=1)),
                ('is_descending', models.BooleanField(default=True)),
                ('image_profile', models.ImageField(blank=True, null=True, upload_to='image/profiles/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]