# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('thread_post', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='tickets/%Y/%m/', null=True, default=None, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField(verbose_name='Date', auto_now_add=True)),
                ('priority', models.CharField(default='1', max_length=20, choices=[('1', 'Low'), ('2', 'Normal'), ('3', 'High'), ('4', 'Urgent')])),
                ('type', models.CharField(default='other', max_length=50, choices=[('help', 'Account Help'), ('billing', 'Billing'), ('bug', 'Bug Report'), ('support', 'Technical Support'), ('other', 'Other (Use if Unsure)')])),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('last_reply_date_time', models.DateTimeField(null=True, default=None, blank=True)),
                ('closed', models.BooleanField(verbose_name='Status', default=False)),
                ('staff_closed', models.BooleanField(default=False)),
                ('unread', models.BooleanField(default=False)),
                ('last_reply_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, default=None, related_name='last_reply_user_id', blank=True, verbose_name='Last Replier')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='thread',
            field=models.ForeignKey(to='tickets.Thread'),
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, default=None, blank=True),
        ),
    ]
