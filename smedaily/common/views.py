from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from smedaily.dart.models import DartSearchData
from smedaily.stocks.models import StocksSignal
from datetime import datetime


# Create your views here.
def index(request):
    return redirect(reverse('login'))


def user_login(request):
    if request.method == 'GET':
        if not request.user.is_authenticated:
            next_page = request.GET.get('next', '/home')
            return render(request, 'login.html', context={'next': next_page})
        else:
            return redirect(reverse('home'))
    elif request.method == 'POST':
        username = request.POST.get('id', '')
        password = request.POST.get('password', '')
        next_page = request.POST.get('next', '')
        print(next_page)
        user = authenticate(username=username, password=password)
        if user:
            login(request, user=user)
            return redirect(next_page)
        else:
            redirect_path = '{}?next='.format(reverse('login')) + next_page
            return redirect(redirect_path)


@login_required(login_url='/login')
def user_logout(request):
    logout(request)
    return redirect(reverse('login'))


@login_required(login_url='/login')
def home(request):
    if request.user.is_anonymous:
        return redirect(reverse('login'))
    today = datetime.now()
    data = DartSearchData.objects.all().order_by('-created_at')[:5]
    signal = StocksSignal.objects.filter(date=today.date()).order_by('-time')[:5]
    context = {
        'darts': data,
        'signals': signal,
        'now':  today
    }
    return render(request, 'home.html', context=context)
