# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_profile_information'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='information',
        ),
    ]
