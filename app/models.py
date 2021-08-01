# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import JSONField

# Create your models here.


class Fields(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    coord = models.JSONField(blank=True, null=True)
    last_obstime = models.DateTimeField(blank=True, null=True)
    last_obstel = models.IntegerField(blank=True, null=True)
    total_times = models.IntegerField(blank=True, null=True)
    history = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'fields'


class Images(models.Model):
    id = models.IntegerField(primary_key=True)
    filename = models.CharField(max_length=100, blank=True, null=True)
    filepath = models.CharField(max_length=200, blank=True, null=True)
    telid = models.IntegerField(blank=True, null=True)
    plan = models.CharField(max_length=30, blank=True, null=True)
    usrid = models.IntegerField(blank=True, null=True)
    datetime = models.DateTimeField(blank=True, null=True)
    date = models.CharField(max_length=8, blank=True, null=True)
    ra = models.FloatField(blank=True, null=True)
    dec = models.FloatField(blank=True, null=True)
    mag_limit = models.FloatField(blank=True, null=True)
    astrometry = models.IntegerField(blank=True, null=True)
    meta = models.JSONField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'images'


class Logs(models.Model):
    id = models.IntegerField(primary_key=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=30, blank=True, null=True)
    level = models.CharField(max_length=10, blank=True, null=True)
    message = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'logs'


class Plans(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    mode = models.IntegerField(blank=True, null=True)
    priority = models.IntegerField(blank=True, null=True)
    tel_id = models.CharField(max_length=10, blank=True, null=True)
    usr_id = models.IntegerField(blank=True, null=True)
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    request_fields = models.JSONField(blank=True, null=True)
    guide_data = models.JSONField(blank=True, null=True)
    progress = models.IntegerField(blank=True, null=True)
    datapath = models.CharField(max_length=200, blank=True, null=True)
    proposal = models.IntegerField(blank=True, null=True)
    history = models.CharField(max_length=1000, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'plans'


class Status(models.Model):
    id = models.IntegerField(primary_key=True)
    heartbeat = models.DateTimeField(blank=True, null=True)
    plan_name = models.CharField(max_length=30, blank=True, null=True)
    mount_status = models.CharField(max_length=20, blank=True, null=True)
    ra = models.FloatField(blank=True, null=True)
    dec = models.FloatField(blank=True, null=True)
    target_ra = models.FloatField(blank=True, null=True)
    target_dec = models.FloatField(blank=True, null=True)
    mount_info = models.JSONField(blank=True, null=True)
    cam_status = models.CharField(max_length=20, blank=True, null=True)
    filter = models.CharField(max_length=5, blank=True, null=True)
    ccd_temp = models.IntegerField(blank=True, null=True)
    cooling_power = models.IntegerField(blank=True, null=True)
    cam_info = models.JSONField(blank=True, null=True)
    free_space = models.FloatField(blank=True, null=True)
    run_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'
