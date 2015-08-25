# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20150823_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='notification_billing',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='notification_lead',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='notification_ticket',
            field=models.IntegerField(default=0),
        ),
    ]
