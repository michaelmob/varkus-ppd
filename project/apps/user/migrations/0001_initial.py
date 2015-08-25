# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0014_auto_20150822_2329'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='Earnings',
            fields=[
                ('leads', models.IntegerField(default=0)),
                ('today', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('yesterday', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('week', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('month', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('yestermonth', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('year', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_today', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_month', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('clicks', models.IntegerField(default=0)),
                ('clicks_hourly', models.CharField(default='', max_length=250, null=True, blank=True)),
                ('obj', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('wallet', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('minimum_payout', models.DecimalField(decimal_places=2, default='10.00', max_digits=5)),
                ('cut_amount', models.DecimalField(max_digits=5, decimal_places=2, default='0.30', help_text='This percentage is taken off of the users payout -- The developers cut', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
                ('referral_cut_amount', models.DecimalField(max_digits=5, decimal_places=2, default='0.10', help_text='This and cut_amount should not sum up to be more than 100% (or 1)', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)])),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('country', models.CharField(max_length=100, null=True, blank=True)),
                ('website', models.URLField(max_length=100, null=True, blank=True)),
                ('offer_block', models.ManyToManyField(to='offers.Offer', related_name='offer_block', blank=True)),
                ('offer_priority', models.ManyToManyField(to='offers.Offer', related_name='offer_priority', blank=True)),
                ('party', models.ForeignKey(default=None, null=True, to='user.Party', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Referral_Earnings',
            fields=[
                ('leads', models.IntegerField(default=0)),
                ('today', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('yesterday', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('week', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('month', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('yestermonth', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('year', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_today', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_month', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('real_total', models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)),
                ('clicks', models.IntegerField(default=0)),
                ('clicks_hourly', models.CharField(default='', max_length=250, null=True, blank=True)),
                ('obj', models.OneToOneField(serialize=False, to=settings.AUTH_USER_MODEL, primary_key=True)),
            ],
            options={
                'verbose_name': 'Referral Earnings',
                'verbose_name_plural': 'Referral Earnings',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='referrer',
            field=models.ForeignKey(default=None, related_name='referrer_id', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
