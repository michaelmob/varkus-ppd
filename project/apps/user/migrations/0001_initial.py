# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from decimal import Decimal
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        ('offers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
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
                ('obj', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('wallet', models.DecimalField(decimal_places=2, max_digits=10, default=Decimal('0'))),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=50)),
                ('minimum_payout', models.DecimalField(decimal_places=2, max_digits=5, default='10.00')),
                ('cut_amount', models.DecimalField(decimal_places=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], max_digits=5, default='0.30', help_text='This percentage is taken off of the users payout -- The developers cut')),
                ('referral_cut_amount', models.DecimalField(decimal_places=2, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], max_digits=5, default='0.10', help_text='This and cut_amount should not sum up to be more than 100% (or 1)')),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
                ('birthday', models.DateField(null=True, blank=True)),
                ('country', models.CharField(null=True, max_length=100, blank=True)),
                ('website', models.URLField(null=True, max_length=100, blank=True)),
                ('notification_ticket', models.IntegerField(default=0)),
                ('notification_lead', models.IntegerField(default=0)),
                ('notification_billing', models.IntegerField(default=0)),
                ('offer_block', models.ManyToManyField(to='offers.Offer', related_name='offer_block', blank=True)),
                ('offer_priority', models.ManyToManyField(to='offers.Offer', related_name='offer_priority', blank=True)),
                ('party', models.ForeignKey(to='user.Party', null=True, default=None, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Referral_Earnings',
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
                ('obj', models.OneToOneField(to=settings.AUTH_USER_MODEL, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'Referral Earnings',
                'verbose_name_plural': 'Referral Earnings',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='referrer',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True, default=None, blank=True, related_name='referrer_id'),
        ),
    ]
