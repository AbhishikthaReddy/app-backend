# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-20 17:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0002_auto_20170118_0956'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billingaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]