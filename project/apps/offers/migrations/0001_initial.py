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
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('offer_id', models.IntegerField()),
                ('priority', models.BooleanField(default=False)),
                ('name', models.CharField(verbose_name='Name', max_length=250)),
                ('anchor', models.CharField(verbose_name='Anchor', max_length=1000)),
                ('requirements', models.CharField(verbose_name='Requirements', max_length=1000)),
                ('user_agent', models.CharField(verbose_name='User Agent', blank=True, default='', max_length=50)),
                ('category', models.CharField(verbose_name='Category', blank=True, null=True, choices=[('Android', 'Android'), ('Downloads', 'Downloads'), ('Email Submits', 'Email Submits'), ('Free', 'Free'), ('Gifts', 'Gifts'), ('Hard Incentives', 'Hard Incentives'), ('Health & Beauty', 'Health & Beauty'), ('Home & Garden', 'Home & Garden'), ('iOS Devices', 'iOS Devices'), ('iPad', 'iPad'), ('iPhone', 'iPhone'), ('Lead Gen', 'Lead Gen'), ('Mobile WAP', 'Mobile WAP'), ('Online Services', 'Online Services'), ('PIN Submit', 'PIN Submit'), ('Samsung devices', 'Samsung devices'), ('Special Requests', 'Special Requests'), ('Surveys', 'Surveys'), ('', '')], max_length=50)),
                ('earnings_per_click', models.DecimalField(verbose_name='EPC', max_digits=15, decimal_places=2)),
                ('country', models.CharField(max_length=747)),
                ('flag', models.CharField(verbose_name='Country', max_length=3)),
                ('country_count', models.IntegerField()),
                ('payout', models.DecimalField(verbose_name='Payout', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('difference', models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('tracking_url', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('leads', models.IntegerField(default=0)),
                ('clicks', models.IntegerField(verbose_name='Clicks', default=0)),
                ('today', models.DecimalField(verbose_name='Today', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('yesterday', models.DecimalField(verbose_name='Yesterday', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('week', models.DecimalField(verbose_name='Week', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('month', models.DecimalField(verbose_name='Month', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('yestermonth', models.DecimalField(verbose_name='Last Month', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('year', models.DecimalField(verbose_name='Year', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('total', models.DecimalField(verbose_name='Total', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('real_today', models.DecimalField(verbose_name='*Today', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('real_month', models.DecimalField(verbose_name='*Month', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('real_total', models.DecimalField(verbose_name='*Total', default=Decimal('0'), max_digits=10, decimal_places=2)),
                ('obj', models.OneToOneField(primary_key=True, to='offers.Offer', serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
    ]
