# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-30 19:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0003_auto_20180429_1751'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccountRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accept', models.BooleanField(default=False)),
                ('userFrom', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userFrom', to=settings.AUTH_USER_MODEL)),
                ('userTo', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userTo', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='activated',
        ),
    ]
