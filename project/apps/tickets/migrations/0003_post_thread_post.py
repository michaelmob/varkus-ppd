# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_remove_post_thread_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='thread_post',
            field=models.BooleanField(default=False),
        ),
    ]
