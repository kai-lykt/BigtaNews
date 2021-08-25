from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
import plotly.graph_objects as go
import plotly.offline as opy
from .models import DetailInfo, BasicInfo, StocksSignal, StockReports
from smedaily.dart.models import FinancialStatement
from smedaily.fusioncharts import FusionCharts
import json
from datetime import date, datetime


@login_required(login_url='/login')
def home(request):
    today = datetime.now()
    signals = StocksSignal.objects.filter(date=today.date()).order_by('-time')
    context = {
        'signals': signals,
        'now': today
    }
    return render(request, 'stock.html', context=context)


@login_required(login_url='/login')
def search(request, page_num):
    search_name = request.GET.get('searchName', '')
    if search_name == '':
        data = BasicInfo.objects.all().order_by('name')
    else:
        data = BasicInfo.objects.filter(name__contains=search_name).order_by('name')

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
    return render(request, 'stocksearch.html', context=context)


@login_required(login_url='/login')
def detail(request, code):
    s = DetailInfo.objects.filter(
        code__code__contains=code,
    ).order_by('-created_at')
    basic_info = BasicInfo.objects.get(code__contains=code)
    financial = FinancialStatement.objects.filter(corp_code=basic_info.corp_code)

    financial_data = {}
    financial_account = [
        {'name': '매출', 'div': ['CIS', 'IS'], 'account_id': ['ifrs-full_Revenue', 'ifrs_Revenue']},
        {'name': '영업이익', 'div': ['CIS', 'IS'], 'account_id': ['dart_OperatingIncomeLoss']},
        {'name': '당기순이익', 'div': ['CIS', 'IS'], 'account_id': ['ifrs-full_ProfitLoss', 'ifrs_ProfitLoss']},
        {'name': '자본총계', 'div': ['BS'], 'account_id': ['ifrs-full_Equity', 'ifrs_Equity']},
        {'name': 'EPS', 'div': ['CIS', 'IS'], 'account_id': ['ifrs-full_BasicEarningsLossPerShare', 'ifrs_BasicEarningsLossPerShare']},
        {'name': '부채총계', 'div': ['BS'], 'account_id': ['ifrs-full_Liabilities', 'ifrs_Liabilities']},
        {'name': '유동부채', 'div': ['BS'], 'account_id': ['ifrs-full_CurrentLiabilities', 'ifrs_CurrentLiabilities']},
        # {'name': '당좌자산', 'div': ['BS'], 'account_id': []},
        {'name': '당좌자산', 'div': ['BS'], 'account_id': ['ifrs-full_CurrentAssets', 'ifrs_CurrentAssets', 'ifrs-full_Inventories', 'ifrs_Inventories']},
        # {'name': '재고자산', 'div': ['BS'], 'account_id': ['ifrs-full_Inventories', 'ifrs_Inventories']},
        {'name': '자본금', 'div': ['BS'], 'account_id': ['ifrs-full_IssuedCapital', 'ifrs_IssuedCapital']},
        # {'name': '자본잉여금', 'div': ['BS'], 'account_id': ['dart_CapitalSurplus']},
        {'name': '잉여금', 'div': ['BS'], 'account_id': ['ifrs-full_RetainedEarnings', 'ifrs_RetainedEarnings', 'dart_CapitalSurplus']},
    ]
    report_code = {
        '사업': '11011',
        '3분기': '11014',
        '반기': '11012',
        '1분기': '11013',
    }

    # 영업이익률 = 영업이익/매출*100
    # 순이익률 = 당기순이익/매출*100
    # ROE = 당기순이익/자본총액 = EPS/BPS

    # EPS = 당기순이익/주식수
    # PER = 시가총액/당기순이익 = 현재주가/EPS
    # BPS = 자본총액/주식수 = EPS/당기순이익*자본총액
    # PBR = 시가총액/자본총액 = 현재주가/BPS = 현재주가/EPS*당기순이익/자본총액

    for account in financial_account:
        # if account['name'] == '당좌자산':
        #     fa = financial.filter(subject_div__in=account['div'], account_name__contains='자산')
        # else:
        fa = financial.filter(subject_div__in=account['div'], account_id__in=account['account_id'])
        d = []
        for y in range(date.today().year, date.today().year-4, -1):
            for key, value in report_code.items():
                fay = fa.filter(business_year=str(y), report_code=value)
                if account['name'] == '잉여금':
                    d.append(sum(x.this_term_amount for x in fay))
                elif account['name'] == '당좌자산':
                    d.append(sum((-1 * x.this_term_amount if 'Inventories' in x.account_id else x.this_term_amount for x in fay)))
                else:
                    d.append(fay[0].this_term_amount if len(fay) > 0 else '')
        financial_data[account['name']] = d

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

    context = {
        'name': basic_info.name,
        'stocks': stocks,
        'plot': chart_obj.render(),
        'financial': financial_data,
        'year': date.today().year,
    }

    return render(request, 'stockdetail.html', context=context)


def api_test(request):
    print(request.POST)
    return None


def get_report_no_page(request):
    return redirect('get_report', page_num=1)


@login_required(login_url='/login')
def get_report(request, page_num):
    stock = request.GET.get('stock', '')
    if stock == '':
        data = StockReports.objects.all().order_by('-date').order_by('-created_at')
    else:
        data = StockReports.objects.filter(stock_name__icontains=stock).order_by('-date').order_by('id')

    pages = Paginator(data, 10)
    page = pages.page(page_num)
    ten_pages = list(range(int((page_num - 1) / 10) * 10 + 1, (
        pages.num_pages + 1 if (int((page_num - 1) / 10) + 1) * 10 > pages.num_pages else (int(
            (page_num - 1) / 10) + 1) * 10 + 1)))

    context = {
        'reports': page,
        'current_page': page_num,
        'total_page': pages.num_pages,
        'has_next': page.has_next(),
        'has_previous': page.has_previous(),
        'ten_pages': ten_pages
    }
    return render(request, 'report.html', context=context)
