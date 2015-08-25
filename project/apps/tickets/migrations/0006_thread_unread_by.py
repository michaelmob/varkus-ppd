# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0005_post_thread_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='unread_by',
            field=models.ForeignKey(null=True, to=settings.AUTH_USER_MODEL, blank=True, default=None, related_name='unread_by_user_id'),
        ),
    ]
