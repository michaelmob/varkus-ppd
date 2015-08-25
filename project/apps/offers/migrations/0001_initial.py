# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('offer_id', models.IntegerField()),
                ('priority', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=150)),
                ('anchor', models.CharField(max_length=500)),
                ('requirements', models.CharField(max_length=500)),
                ('user_agent', models.CharField(blank=True, max_length=50, default='')),
                ('category', models.CharField(blank=True, choices=[('Android', 'Android'), ('Downloads', 'Downloads'), ('Email Submits', 'Email Submits'), ('Free', 'Free'), ('Gifts', 'Gifts'), ('Hard Incentives', 'Hard Incentives'), ('Health & Beauty', 'Health & Beauty'), ('Home & Garden', 'Home & Garden'), ('iOS Devices', 'iOS Devices'), ('iPad', 'iPad'), ('iPhone', 'iPhone'), ('Lead Gen', 'Lead Gen'), ('Mobile WAP', 'Mobile WAP'), ('Online Services', 'Online Services'), ('PIN Submit', 'PIN Submit'), ('Samsung devices', 'Samsung devices'), ('Special Requests', 'Special Requests'), ('Surveys', 'Surveys'), ('', '')], max_length=50, null=True)),
                ('earnings_per_click', models.DecimalField(decimal_places=2, max_digits=15)),
                ('country', models.CharField(max_length=747)),
                ('flag', models.CharField(max_length=3)),
                ('country_count', models.IntegerField()),
                ('payout', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('difference', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('tracking_url', models.CharField(max_length=300)),
                ('clicks', models.IntegerField(default=0)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('leads', models.IntegerField(default=0)),
                ('today', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('yesterday', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('week', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('month', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('yestermonth', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('year', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('real_today', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('real_month', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('real_total', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('obj', models.OneToOneField(primary_key=True, to='offers.Offer', serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
    ]
