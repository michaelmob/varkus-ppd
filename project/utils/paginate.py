from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def pages(objects, count, num=1):
	paginator = Paginator(objects, count)

	try:
		return paginator.page(num)
	except PageNotAnInteger:
		return paginator.page(1)
	except EmptyPage:
		return paginator.page(paginator.num_pages)
