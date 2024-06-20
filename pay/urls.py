from django.urls import path
from . import views,FastPay,Goopagoo,hkpPay,SitoBank
urlpatterns = [
    path('payrequest/<int:uid>/<int:shopId>/<int:price>/<int:channelNo>/<str:paytype>',views.payrequest),
    path('payrequestUrl/<int:uid>/<int:shopId>/<int:price>/<int:channelNo>',views.payrequestUrl),
    path('kwViewContent/<int:uid>',views.kwViewContent),
    path('testCallBackUp/',views.testCallBackUp),
    #添加外围回调接口
    path('FastPayCallBack',FastPay.FastPayCallBack),
    path('goopagooPayCallBack',Goopagoo.goopagooPayCallBack),
    path('hkpPayCallBack',hkpPay.hkpPayCallBack),
    path('SitoBankCallBack',SitoBank.SitoBankCallBack),
    #path('FastPayTestBack',FastPay.FastPayTestBack),
]
