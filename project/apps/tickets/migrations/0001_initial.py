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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('ip_address', models.GenericIPAddressField()),
                ('date_time', models.DateTimeField()),
                ('priority', models.CharField(default='1', max_length=20, choices=[('1', 'Low'), ('2', 'Normal'), ('3', 'High'), ('4', 'Urgent')])),
                ('type', models.CharField(default='other', max_length=50, choices=[('help', 'Account Help'), ('billing', 'Billing'), ('bug', 'Bug Report'), ('support', 'Technical Support'), ('other', 'Other (Use if Unsure)')])),
                ('subject', models.CharField(max_length=100)),
                ('last_reply_date_time', models.DateTimeField(null=True, blank=True, default=None)),
                ('closed', models.BooleanField(default=False)),
                ('staff_closed', models.BooleanField(default=False)),
                ('last_reply_user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, default=None, related_name='last_reply_user_id')),
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
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, blank=True, default=None),
        ),
    ]
