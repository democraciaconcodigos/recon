#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resources for models api.
"""
from django.conf.urls import patterns, include, url
from tastypie.resources import ModelResource
from tgp.models import Telegram, Table, Cell

"""Seccion / circuito / mesa
"""


class TelegramResource(ModelResource):
    class Meta:
        queryset = Telegram.objects.all()
        resource_name = 'telegrama'
        detail_uri_name = 'section'

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<section>[\d]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

#class TableResource(ModelResource):
#    class Meta:
#        queryset = Table.objects.all()
        #resource_name = 'table'

