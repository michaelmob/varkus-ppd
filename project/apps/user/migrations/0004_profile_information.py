# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20150823_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='information',
            field=models.BooleanField(default=False, help_text='Please use the following format: <em>YYYY-MM-DD</em>.'),
        ),
    ]
