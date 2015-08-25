# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0012_auto_20150819_0039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='earnings',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
    ]
