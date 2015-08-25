# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0005_remove_earnings_clicks_hourly'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='clicks_hourly',
            field=models.CharField(null=True, default='', blank=True, max_length=250),
        ),
    ]
