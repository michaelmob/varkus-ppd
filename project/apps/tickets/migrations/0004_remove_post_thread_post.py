# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_post_thread_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thread_post',
        ),
    ]
