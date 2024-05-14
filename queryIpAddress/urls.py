from django.urls import path
from . import views
urlpatterns = [
    path('get/<str:mechine>',views.get),
    path('get/',views.get1),
    path('queryUidByAdid/<str:adid>',views.queryUidByAdid),
    path('addMechine/<str:mechine>',views.addMechine),
    path('IsRedJump/',views.IsRedJump)
]

views.readIpZoneCfg()