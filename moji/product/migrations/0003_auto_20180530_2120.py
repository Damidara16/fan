# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-31 01:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_auto_20180522_1514'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('stripe_id', models.CharField(default='', max_length=80)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RenameField(
            model_name='plan',
            old_name='name',
            new_name='nickname',
        ),
        migrations.AddField(
            model_name='plan',
            name='stripe_id',
            field=models.CharField(default='', max_length=80),
        ),
    ]
