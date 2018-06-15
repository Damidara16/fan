# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-01 00:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_profile_following'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountrequest',
            name='userFrom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requester', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='accountrequest',
            name='userTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
