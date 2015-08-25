# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_remove_offer_difference'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='difference',
            field=models.DecimalField(max_digits=10, default=Decimal('0'), decimal_places=2),
        ),
    ]
