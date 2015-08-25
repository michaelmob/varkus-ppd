# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0013_auto_20150819_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='clicks_hourly',
            field=models.CharField(blank=True, default='', max_length=250, null=True),
        ),
    ]
