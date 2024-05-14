"""webapi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('pay/',include('pay.urls')),                   #支付
    path('repay/',include('repay.urls')),                            #代付
    path('relation/',include('relation.urls')),
    path('sms/',include('sms.urls')),                   #短信
    path('queryIpAddress/',include('queryIpAddress.urls')),#查询IP归属地
    path('adjustData/',include('adjustData.urls')),
    path('imageUp/',include('imageUpLoad.urls')),
    path('gamelog/',include('gamelog.urls')),
]
