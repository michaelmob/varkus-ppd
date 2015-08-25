# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0011_remove_earnings_real_nig'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='clicks',
        ),
        migrations.AddField(
            model_name='earnings',
            name='clicks',
            field=models.IntegerField(max_length=10, default=0),
        ),
        migrations.AddField(
            model_name='earnings',
            name='clicks_hourly',
            field=models.CharField(max_length=250, default=''),
        ),
    ]
