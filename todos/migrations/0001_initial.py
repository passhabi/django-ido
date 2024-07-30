# Generated by Django 5.0.6 on 2024-07-30 20:23

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
            name='Todolist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=300)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateTimeField(blank=True, null=True)),
                ('priority', models.SmallIntegerField(blank=True, choices=[(1, 'Important and Urgent'), (2, 'Important'), (3, 'Urgent'), (4, 'Not Urgent, Important')], null=True)),
                ('category', models.IntegerField(blank=True, null=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('completion_time', models.DateTimeField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
