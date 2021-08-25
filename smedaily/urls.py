"""smedaily URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from smedaily.common import views as common_views
from smedaily.dart import views as dart_views
from smedaily.stocks import views as stock_views
from smedaily.article import views as article_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('summernote/', include('django_summernote.urls')),

    path('', common_views.index, name='index'),
    path('login', common_views.user_login, name='login'),
    path('logout', common_views.user_logout, name='logout'),

    path('home', common_views.home, name='home'),

    path('dart', dart_views.home, name='dart_home'),
    path('dart/<int:page_num>', dart_views.dart_page, name='dart_page'),
    path('dart/search_company', dart_views.search_company, name='search_company'),

    path('stock', stock_views.home, name='stock_home'),
    path('stock/search/<int:page_num>', stock_views.search, name='stock_search'),
    path('stock/detail/<str:code>', stock_views.detail, name='stock_detail'),

    path('report', stock_views.get_report_no_page, name='get_report_no_page'),
    path('report/<int:page_num>', stock_views.get_report, name='get_report'),

    path('article', article_views.home, name='article_home'),
    path('article/<int:page_num>', article_views.article_page, name='article_page'),
    path('article/view/<int:article_id>', article_views.article_view, name='article_view'),
    path('article/write', article_views.article_write, name='article_write'),

    path('api/test1', stock_views.api_test, name='apistest'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, insecure=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
