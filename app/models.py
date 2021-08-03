# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.db import models
from django.contrib.auth.models import User
import json


class JSONFieldJSONType(models.JSONField):
    """
    Custom JSON field because our postgres uses json type and not jsonb.

    Details on these changes within Django can be seen here:

    * https://code.djangoproject.com/ticket/31973
    * https://code.djangoproject.com/ticket/31956#comment:8

    PR that changed behavior for regular json type:
    https://github.com/django/django/commit/0be51d2226fce030ac9ca840535a524f41e9832c

    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        # Some backends (SQLite at least) extract non-string values in their
        # SQL datatypes.
        # if isinstance(expression, KeyTransform) and not isinstance(value, str):
        if not isinstance(value, str):
            return value
        try:
            # Custom implementation for how our data comes out of our postgres
            # connection.
            if isinstance(value, dict):
                data_value = self.get_prep_value(value)
            else:
                data_value = value
            return json.loads(data_value, cls=self.decoder)
        except json.JSONDecodeError:
            return value

# Create your models here.


class Fields(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    coord = JSONFieldJSONType(blank=True, null=True)
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
    meta = JSONFieldJSONType(blank=True, null=True)

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
    request_fields = JSONFieldJSONType(blank=True, null=True)
    guide_data = JSONFieldJSONType(blank=True, null=True)
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
    mount_info = JSONFieldJSONType(blank=True, null=True)
    cam_status = models.CharField(max_length=20, blank=True, null=True)
    filter = models.CharField(max_length=5, blank=True, null=True)
    ccd_temp = models.IntegerField(blank=True, null=True)
    cooling_power = models.IntegerField(blank=True, null=True)
    cam_info = JSONFieldJSONType(blank=True, null=True)
    free_space = models.FloatField(blank=True, null=True)
    run_level = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'status'
