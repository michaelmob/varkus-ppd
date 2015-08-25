# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0008_earnings_clicks_hr'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='earnings',
            name='clicks_hr',
        ),
        migrations.AddField(
            model_name='earnings',
            name='fffffffff',
            field=models.CharField(default='', max_length=250, blank=True, null=True),
        ),
    ]
