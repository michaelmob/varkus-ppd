# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0009_auto_20150818_1605'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='earnings',
            name='fffffffff',
        ),
        migrations.AddField(
            model_name='earnings',
            name='real_nig',
            field=models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0')),
        ),
    ]
