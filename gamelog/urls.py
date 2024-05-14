from django.urls import path
from . import views,cashback,teamcashback
urlpatterns = [
    path('GetToltalGameRecord/<int:uid>/<int:sTime>/<int:eTime>',views.GetToltalGameRecord),
    path('GetListGameRecord/<int:uid>/<int:curPage>/<int:sTime>/<int:eTime>',views.GetListGameRecord),
    path('GetGameDetailList/<int:uid>/<int:gameId>/<int:curPage>/<int:sTime>/<int:eTime>',views.GetGameDetailList),

    path('getIndexData/<int:uid>',cashback.getIndexData),
    path('getTimeRandData/<int:uid>/<int:sTime>/<int:eTime>',cashback.getTimeRandData),
    path('getTimeRandDetailData/<int:uid>/<int:curPage>/<int:sTime>/<int:eTime>',cashback.getTimeRandDetailData),

    path('getTeamCashBack/<int:uid>',teamcashback.getTeamCashBack),
    path('getLowDetail/<int:uid>/<int:curPage>',teamcashback.getLowDetail)
]