# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0003_offer_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='earnings',
            name='clicks_hourly',
            field=models.CharField(default='', max_length=250, null=True, blank=True),
        ),
    ]
