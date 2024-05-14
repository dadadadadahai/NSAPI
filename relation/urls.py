from django.urls import path
from . import views,queryViews
urlpatterns = [
    #绑定哦处理
    path('bind/<str:parentInviter>/<str:uidInviter>',views.bind),
    #查询其他数据
    path('queryNumVal/<int:uid>',queryViews.queryNumVal),
    path('queryMaxRebateBelow/<int:uid>/<int:page>',queryViews.queryMaxRebateBelow),
    path('queryLog/<int:uid>/<int:page>',queryViews.queryLog),
    path('queryChipLog/<int:uid>/<int:page>',queryViews.queryChipLog),
    path('queryCurDayInfo/<int:uid>/<int:page>',queryViews.queryCurDayInfo),
    path('queryvalidinvitelog/<int:uid>/<int:page>',queryViews.queryvalidinvitelog),
    path('queryvalidinvitelogDay/<int:uid>/<int:page>',queryViews.queryvalidinvitelogDay),
]