from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import DartSearchData, CorpBasicData
from smedaily.stocks.models import BasicInfo
from datetime import date, timedelta


@login_required(login_url='/login')
def home(request):
    return redirect('dart_page', page_num=1)


@login_required(login_url='/login')
def dart_page(request, page_num):
    data_type = request.GET.getlist('data_type', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
    from_date = request.GET.get('fromDate', date.today() - timedelta(7))
    to_date = request.GET.get('toDate', date.today())

    corp_names = list(filter(lambda name: name != '', request.GET.get('corp_name', '').split(',')))
    stock_codes = list(filter(lambda name: name != '', request.GET.get('stockCode', '').split(',')))
    if len(corp_names) == 0:
        data = DartSearchData.objects.filter(
            data_date__range=(from_date, to_date),
            data_type__in=data_type
        ).order_by('-created_at')
    else:
        data = DartSearchData.objects.filter(
            data_date__range=(from_date, to_date),
            stock_code__in=stock_codes,
            data_type__in=data_type
        ).order_by('-created_at')

    pages = Paginator(data, 10)
    page = pages.page(page_num)
    ten_pages = list(range(int((page_num - 1) / 10) * 10 + 1, (
        pages.num_pages + 1 if (int((page_num - 1) / 10) + 1) * 10 > pages.num_pages else (int(
            (page_num - 1) / 10) + 1) * 10 + 1)))

    context = {
        'data': page,
        'current_page': page_num,
        'total_page': pages.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'ten_pages': ten_pages
    }
    # context = {
    #     'data': [],
    #     'current_page': page_num,
    #     'total_page': 1,
    #     'has_next': False,
    #     'has_previous': False,
    #     'ten_pages': [1],
    #     'corps': []
    # }
    return render(request, 'dart.html', context=context)


def search_company(request):
    search_name = request.POST.get('search_name', '')
    corp_type = request.POST.get('corp_type', 'Z')
    page_num = request.POST.get('page', 1)
    # print(search_name, corp_type, page_num)
    if corp_type == 'Z':
        if search_name == '':
            data = CorpBasicData.objects.all().order_by('corp_name')
        else:
            data = CorpBasicData.objects.filter(corp_name__icontains=search_name).order_by('corp_name')
    else:
        if search_name == '':
            data = CorpBasicData.objects.filter(corp_type=corp_type).order_by('corp_name')
        else:
            data = CorpBasicData.objects.filter(corp_name__icontains=search_name, corp_type=corp_type).order_by('corp_name')

    pages = Paginator(data, 10)
    page = pages.page(page_num)
    three_pages = list(range(int((page_num - 1) / 3) * 3 + 1, (
        pages.num_pages + 1 if (int((page_num - 1) / 3) + 1) * 3 > pages.num_pages else (int(
            (page_num - 1) / 3) + 1) * 3 + 1)))

    d = [{'corp_name': a.corp_name, 'ceo_name': a.ceo_name, 'stock_code': a.stock_code, 'industry_code': a.industry_code} for a in list(page)]

    context = {
        'total_num': len(data),
        'data': d,
        'page_num': page_num,
        'total_page': pages.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'three_pages': three_pages
    }
    return JsonResponse(context)
