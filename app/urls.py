# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('telescopes.html', views.telescopes, name='telescopes'),
    path('plans.html', views.plans, name='plans'),
    path('logs.html', views.logs, name='logs'),
    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),

]
