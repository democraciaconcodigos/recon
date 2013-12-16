#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Urls for telegram parser app.
"""
from django.conf.urls import patterns, include, url

#from tastypie.api import Api
#from tgp.api import TelegramResource

#telegram_resource = TelegramResource()

urlpatterns = patterns('',
#    (r'^', include(telegram_resource.urls)),
    url(r'^telegrama/(\d{3})/(\d{4})/(\d{4})/$', 'tgp.views.telegram_detail'),
)


