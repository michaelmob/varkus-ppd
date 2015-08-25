# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='notification_billing',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='notification_lead',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='profile',
            name='notification_ticket',
            field=models.BooleanField(default=False),
        ),
    ]
