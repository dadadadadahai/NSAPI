from django.urls import path
from . import views
urlpatterns = [
    path('send/<str:code>/<str:phone>',views.send),
]