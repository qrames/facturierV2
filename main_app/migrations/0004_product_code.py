# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-10-04 13:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_quotation_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='code',
            field=models.IntegerField(default=0),
        ),
    ]
