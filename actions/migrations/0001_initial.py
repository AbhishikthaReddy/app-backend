# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-06 13:19
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Action',
            fields=[
                ('path', models.CharField(max_length=255)),
                ('payload', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('action', models.CharField(db_index=True, max_length=100)),
                ('method', models.CharField(max_length=7)),
                ('user_agent', models.CharField(max_length=255)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('state', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'In Progress'), (2, 'Canceling'), (3, 'Cancelled'), (4, 'Success'), (5, 'Failed')])),
                ('ip', models.GenericIPAddressField(null=True)),
                ('object_id', models.UUIDField(null=True)),
                ('can_be_cancelled', models.BooleanField(default=False)),
                ('can_be_retried', models.BooleanField(default=False)),
                ('is_user_action', models.BooleanField(default=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.ContentType')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='actions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
