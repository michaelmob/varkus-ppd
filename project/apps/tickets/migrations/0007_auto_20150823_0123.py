# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0006_thread_unread_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='thread',
            name='unread_by',
        ),
        migrations.AddField(
            model_name='thread',
            name='unread',
            field=models.BooleanField(default=False),
        ),
    ]
