from celery import shared_task
from .models import Earnings, Referral_Earnings
from apps.conversions.models import Token
from django.core.cache import cache


@shared_task
def reset_today():
	cache.clear()
	#Token.clear()

	return (Earnings().reset_today(), Referral_Earnings().reset_today())


@shared_task
def reset_week():
	return (Earnings().reset_week(), Referral_Earnings().reset_week())


@shared_task
def reset_month():
	return (Earnings().reset_month(), Referral_Earnings().reset_month())


@shared_task
def reset_year():
	return (Earnings().reset_year(), Referral_Earnings().reset_year())
