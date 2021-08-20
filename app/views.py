# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.contrib.sites import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, JsonResponse
from django import template
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Status, Plans, Logs
from datetime import datetime
import cgi,cgitb
#from django.utils import timezone as datetime
import json


@login_required(login_url="/login/")
def index(request):

    context = {}
    context['segment'] = 'index'

    html_template = loader.get_template('index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def telescopes(request):
    context = {}
    context['segment'] = 'telescopes'
    context['tels'] = Status.objects.using(
        'sensors').order_by('id').all().values()
    for t in context['tels']:
        t['tmdiff'] = (datetime.utcnow() - t['heartbeat']).seconds
        t['cam_info'] = json.dumps(t['cam_info'], indent=2)
        t['mount_info'] = json.dumps(t['mount_info'], indent=2)


    if request.is_ajax():
        data = {'rendered_table': loader.get_template(
            'status_table.html').render(context, request)}
        return JsonResponse(data)


    html_template = loader.get_template('ui-telescopes.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def plans(request):
    context = {}
    context['segment'] = 'plans'
    context['plans'] = Plans.objects.using('sensors').all().values()
    html_template = loader.get_template('ui-plans.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def logs(request):
    context = {}
    context['segment'] = 'logs'

    post_start_time = request.POST.get('start_time', '')[:10]
    if post_start_time == '':
        post_start_time = request.GET.get('start_time', '')[:10]

    post_end_time = request.POST.get('end_time', '')[:10]
    if post_end_time == '':
        post_end_time = request.GET.get('end_time', '')[:10]

    tel_id = request.POST.get('tel_id', '')
    if tel_id == '':
        tel_id = request.GET.get('tel_id', '')

    context['start_time'] = post_start_time
    context['end_time'] = post_end_time
    context['tel_id'] = tel_id


    now_time = datetime.utcnow().date()

    if post_start_time != '':
        start_time = datetime.strptime(post_start_time, '%m/%d/%Y').date()
        if post_end_time != '':
            end_time = datetime.strptime(post_end_time, '%m/%d/%Y').date()
            time_filter_logs = Logs.objects.using('sensors').filter(timestamp__range=(start_time,end_time)).order_by('-timestamp').values()
        else:
            time_filter_logs = Logs.objects.using('sensors').filter(timestamp__range=(start_time, now_time)).order_by('-timestamp').values()

    else:
        time_filter_logs = Logs.objects.using('sensors').filter(timestamp__gte=now_time).order_by('-timestamp').values()

    # filter list to show in the table
    logs = []
    if tel_id == '':
        logs = time_filter_logs

    if tel_id == 'ALL':
        logs = time_filter_logs
    else:
        for log in time_filter_logs:
            if log['source'] == tel_id:
                logs.append(log)

    print(context)
    page_num = int(request.GET.get('page', 1))
    logs_paginator = Paginator(logs, 10)
    try:
        context['logs'] = logs_paginator.page(page_num)
    except PageNotAnInteger:
        context['logs'] = logs_paginator.page(1)
    except EmptyPage:
        context['logs'] = logs_paginator.page(logs_paginator.num_pages)

    #page = request.GET.get('page')
    #logs_p = logs_paginator.get_page(page)
    #context['logs'] = logs_p

    #html_template = loader.get_template('ui-logs.html')
    #print(context)
    return render(request, 'ui-logs.html', context)
    #return HttpResponse(html_template.render(context, request))



@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
