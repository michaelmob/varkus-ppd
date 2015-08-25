# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0007_remove_earnings_clicks_hourly'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='clicks_hr',
            field=models.CharField(default='', null=True, max_length=250, blank=True),
        ),
    ]
