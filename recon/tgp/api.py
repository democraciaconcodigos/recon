#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Resources for models api.
"""
from tastypie.resources import ModelResource
from tgp.models import Telegram, Table, Cell


class TelegramResource(ModelResource):
    class Meta:
        queryset = Telegram.objects.all()

