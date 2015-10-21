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
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('offer_id', models.IntegerField()),
                ('priority', models.BooleanField(default=False)),
                ('name', models.CharField(verbose_name='Name', max_length=250)),
                ('anchor', models.CharField(verbose_name='Anchor', max_length=1000)),
                ('requirements', models.CharField(verbose_name='Requirements', max_length=1000)),
                ('user_agent', models.CharField(verbose_name='User Agent', default='', max_length=50, blank=True)),
                ('category', models.CharField(null=True, verbose_name='Category', max_length=50, choices=[('Android', 'Android'), ('Downloads', 'Downloads'), ('Email Submits', 'Email Submits'), ('Free', 'Free'), ('Gifts', 'Gifts'), ('Hard Incentives', 'Hard Incentives'), ('Health & Beauty', 'Health & Beauty'), ('Home & Garden', 'Home & Garden'), ('iOS Devices', 'iOS Devices'), ('iPad', 'iPad'), ('iPhone', 'iPhone'), ('Lead Gen', 'Lead Gen'), ('Mobile WAP', 'Mobile WAP'), ('Online Services', 'Online Services'), ('PIN Submit', 'PIN Submit'), ('Samsung devices', 'Samsung devices'), ('Special Requests', 'Special Requests'), ('Surveys', 'Surveys'), ('', '')], blank=True)),
                ('earnings_per_click', models.DecimalField(decimal_places=2, max_digits=15, verbose_name='EPC')),
                ('country', models.CharField(max_length=747)),
                ('flag', models.CharField(verbose_name='Country', max_length=5)),
                ('country_count', models.IntegerField()),
                ('payout', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Payout', default=Decimal('0'))),
                ('difference', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
                ('tracking_url', models.CharField(max_length=1000)),
                ('date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('leads', models.IntegerField(default=0)),
                ('clicks', models.IntegerField(verbose_name='Clicks', default=0)),
                ('today', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Today', default=Decimal('0'))),
                ('yesterday', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Yesterday', default=Decimal('0'))),
                ('week', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Week', default=Decimal('0'))),
                ('month', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Month', default=Decimal('0'))),
                ('yestermonth', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Last Month', default=Decimal('0'))),
                ('year', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Year', default=Decimal('0'))),
                ('total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Total', default=Decimal('0'))),
                ('real_today', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='*Today', default=Decimal('0'))),
                ('real_month', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='*Month', default=Decimal('0'))),
                ('real_total', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='*Total', default=Decimal('0'))),
                ('obj', models.OneToOneField(to='offers.Offer', primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
    ]
