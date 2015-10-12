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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thread_post', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField()),
                ('content', models.TextField(max_length=1000)),
                ('image', models.ImageField(blank=True, null=True, default=None, upload_to='tickets/%Y/%m/')),
            ],
        ),
        migrations.CreateModel(
            name='Thread',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField(verbose_name='Date')),
                ('priority', models.CharField(default='1', choices=[('1', 'Low'), ('2', 'Normal'), ('3', 'High'), ('4', 'Urgent')], max_length=20)),
                ('type', models.CharField(default='other', choices=[('help', 'Account Help'), ('billing', 'Billing'), ('bug', 'Bug Report'), ('support', 'Technical Support'), ('other', 'Other (Use if Unsure)')], max_length=50)),
                ('subject', models.CharField(verbose_name='Subject', max_length=100)),
                ('last_reply_date_time', models.DateTimeField(blank=True, null=True, default=None)),
                ('closed', models.BooleanField(verbose_name='Status', default=False)),
                ('staff_closed', models.BooleanField(default=False)),
                ('unread', models.BooleanField(default=False)),
                ('last_reply_user', models.ForeignKey(verbose_name='Last Replier', blank=True, null=True, to=settings.AUTH_USER_MODEL, related_name='last_reply_user_id', default=None)),
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
            field=models.ForeignKey(blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None),
        ),
    ]
