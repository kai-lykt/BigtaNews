from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article
from smedaily.stocks.models import DetailInfo, HistoricData
from django.core.paginator import Paginator
from smedaily.dart.models import DartSearchData
from datetime import date, timedelta
from .parseFile import get_summary, dict_generator
import plotly.graph_objects as go
import plotly.offline as opy
from smedaily.fusioncharts import FusionCharts
import json


@login_required(login_url='/login')
def home(request):
    return redirect('article_page', page_num=1)


@login_required(login_url='/login')
def article_page(request, page_num):
    search_name = request.GET.get('searchName', '')
    if search_name == '':
        data = Article.objects.all().order_by('-created_at')
    else:
        data = Article.objects.filter(title__icontains=search_name).order_by('-created_at')

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

    return render(request, 'article.html', context=context)


@login_required(login_url='/login')
def article_view(request, article_id):
    article = Article.objects.get(id=article_id)
    related_id = list(filter(lambda x: x != '', article.relate_dart.split(',')))
    related_dart = DartSearchData.objects.filter(id__in=related_id).order_by('-created_at')
    summaries = []
    for index, d in enumerate(related_dart):
        summary = []
        for i in dict_generator(get_summary(d.contents)):
            summary.append(i[-1])
        summaries.append({
            'num': index + 1,
            'date': d.data_date,
            'summary': summary,
            'receipt_no': d.receipt_no
        })

    context = {
        'article': article,
        'summaries': summaries,
        'data': related_dart,
    }
    return render(request, 'articleview.html', context=context)


def article_write(request):
    if request.method == 'GET':
        form = ArticleForm()
        page_num = request.GET.get('page', 1)
        data_type = request.GET.getlist('data_type', ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'])
        from_date = request.GET.get('fromDate', date.today())
        to_date = request.GET.get('toDate', date.today())
        stock_code = request.GET.get('stockCode', '')

        if stock_code == '':
            data = []
            s = []
        else:
            data = DartSearchData.objects.filter(
                data_date__range=(from_date, to_date),
                stock_code=stock_code,
                data_type__in=data_type
            ).order_by('-created_at')
            s = DetailInfo.objects.filter(
                code__code__contains=stock_code,
                data_date__range=(from_date, to_date),
            ).order_by('-created_at')

        stocks = []
        chart_data = []
        x_indexes = []
        x_index = len(s)
        for index, a in enumerate(s):
            stocks.append({
                'data_date': a.data_date,
                'current_price': a.current_price,
                'updown_price': a.updown_price,
                'open_price': a.open_price,
                'high_price': a.high_price,
                'low_price': a.low_price,
                'change_percent': round(a.updown_price / (a.current_price - a.updown_price) * 100, 2),
                'volume': a.transaction_volume
            })
            chart_data.append({
                'tooltext': "<b>" + str(a.data_date) + "</b><br>시가: <b>$openDataValue</b><br>종가: <b>$closeDataValue</b><br>고가: <b>$highDataValue</b><br>저가: <b>$lowDataValue</b><br>거래: <b>$volumeDataValue</b>",
                'open': float(a.open_price),
                'high': float(a.high_price),
                'low': float(a.low_price),
                'close': float(a.current_price),
                'volume': a.transaction_volume,
                'x': x_index
            })
            if index % 5 == 0:
                x_indexes.append({
                    'label': str(a.data_date),
                    'x': x_index
                })
            x_index -= 1

        charts = {
            "chart": {
                "pyaxisname": "가격",
                "vyaxisname": "거래량",
                "theme": "fusion",
                "showvolumechart": "1",
                "formatNumber": 1,
                "formatNumberScale": False,
                "bullFillColor": '#e55f5f',
                "bearFillColor": '#5a7be3',
            },
            "categories": [{
                "category": x_indexes
            }],
            "dataset": [{
                "data": chart_data
            }]
        }

        chart_obj = FusionCharts(
            'candlestick',
            'ex1',
            '1152',
            '500',
            'chart-1',
            'json',
            json.dumps(charts, ensure_ascii=False)
        )

        pages = Paginator(data, 10)
        page = pages.page(page_num)
        ten_pages = list(range(int((page_num - 1) / 10) * 10 + 1, (
            pages.num_pages + 1 if (int((page_num - 1) / 10) + 1) * 10 > pages.num_pages else (int(
                (page_num - 1) / 10) + 1) * 10 + 1)))

        summaries = []
        for index, d in enumerate(page.object_list):
            summary = []
            for i in dict_generator(get_summary(d.contents)):
                summary.append(i[-1])
            summaries.append({
                'num': index + 1,
                'date': d.data_date,
                'summary': summary,
                'receipt_no': d.receipt_no
            })

        context = {
            'form': form,
            'data': page,
            'current_page': page_num,
            'total_page': pages.num_pages,
            'has_next': page.has_next(),
            'has_previous': page.has_previous(),
            'ten_pages': ten_pages,
            'stocks': stocks,
            'summaries': summaries,
            'plot': chart_obj.render()
        }
        return render(request, 'articlewrite.html', context)
    elif request.method == 'POST':
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.stock = request.POST.get('stock', ' ')
            article.proto = request.POST.get('protoArticle', ' ')
            article.relate_dart = request.POST.get('dartIds', ' ')
            article.writer = request.user
            article.save()
            return redirect('article_page', page_num=1)
