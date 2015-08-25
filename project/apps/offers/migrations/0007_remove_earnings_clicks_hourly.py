# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0006_earnings_clicks_hourly'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='earnings',
            name='clicks_hourly',
        ),
    ]
