from django.urls import path
from . import views,TsPay,LePay,InterFacePay,FastPay,Goopagoo,hkpPay,SitoBank
urlpatterns = [
    #添加返利推广
    # path('repayRelationAddOrder/<int:uid>',views.repayRelationAddOrder),
    #查询返利订单
    path('repayRebatQuery/<int:uid>/<int:page>',views.repayRebatQuery),
    path('repayState/<int:orderNo>/<int:channelNo>',views.repayState),
    path('TsPayCallBack',TsPay.TsPayCallBack),  #提现TS回调
    path('LePayCallBack',LePay.LePayCallBack),  #提现TS回调
    path('InterFaceCallBack',InterFacePay.InterFaceCallBack),
    path('FastPayCallBack',FastPay.FastPayCallBack),
    path('GoopagPayCallBack',Goopagoo.GoopagPayCallBack),
    path('hkpPayCallBack',hkpPay.hkpPayCallBack),
    path('SitoBankCallBack',SitoBank.SitoBankCallBack),
]