# -*- coding: utf-8 -*-
# -*- author: Jiangtao -*-


from django.urls import path

from . import views


urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<str:lang>/index/', views.index, name='index'),
]
