from django.urls import path
from . import views
urlpatterns = [
    path('index/<int:uid>',views.index),
    path('addIndex/<int:uid>',views.addIndex)
]