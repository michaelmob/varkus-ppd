# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import django.core.validators
from decimal import Decimal


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0006_require_contenttypes_0002'),
        ('offers', '0001_initial'),
    ]

    operations = [
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
                ('obj', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('wallet', models.DecimalField(default=Decimal('0'), max_digits=10, decimal_places=2)),
            ],
            options={
                'verbose_name_plural': 'Earnings',
            },
        ),
        migrations.CreateModel(
            name='Party',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('minimum_payout', models.DecimalField(default='10.00', max_digits=5, decimal_places=2)),
                ('cut_amount', models.DecimalField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], decimal_places=2, default='0.30', max_digits=5, help_text='This percentage is taken off of the users payout -- The developers cut')),
                ('referral_cut_amount', models.DecimalField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], decimal_places=2, default='0.10', max_digits=5, help_text='This and cut_amount should not sum up to be more than 100% (or 1)')),
            ],
            options={
                'verbose_name_plural': 'Parties',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
                ('birthday', models.DateField(blank=True, null=True)),
                ('country', models.CharField(blank=True, null=True, max_length=100)),
                ('website', models.URLField(blank=True, null=True, max_length=100)),
                ('notification_ticket', models.IntegerField(default=0)),
                ('notification_lead', models.IntegerField(default=0)),
                ('notification_billing', models.IntegerField(default=0)),
                ('offer_block', models.ManyToManyField(related_name='offer_block', blank=True, to='offers.Offer')),
                ('offer_priority', models.ManyToManyField(related_name='offer_priority', blank=True, to='offers.Offer')),
                ('party', models.ForeignKey(blank=True, null=True, to='user.Party', default=None)),
            ],
        ),
        migrations.CreateModel(
            name='Referral_Earnings',
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
                ('obj', models.OneToOneField(primary_key=True, to=settings.AUTH_USER_MODEL, serialize=False)),
            ],
            options={
                'verbose_name': 'Referral Earnings',
                'verbose_name_plural': 'Referral Earnings',
            },
        ),
        migrations.AddField(
            model_name='profile',
            name='referrer',
            field=models.ForeignKey(related_name='referrer_id', blank=True, null=True, to=settings.AUTH_USER_MODEL, default=None),
        ),
    ]
