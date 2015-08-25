# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0010_auto_20150818_1606'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='earnings',
            name='real_nig',
        ),
    ]
