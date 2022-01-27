# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views




urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('ui-telescopes.html', views.telescopes, name='telescopes'),
    path('ui-plans.html', views.plans, name='plans'),
    path('ui-logs.html', views.logs, name='logs'),
    path('socket_test.html',views.chat,name='socket_test'),
    #path('<str:room_name>/', views.room, name='room'),
    # Matches any html file
    #re_path(r'^.*\.*', views.pages, name='pages'),



]
