# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

UPLOAD_TO = settings.MEDIA_ROOT

class Telegram(models.Model):
    id = models.CharField(max_length=30, unique=True, db_index=True, primary_key=True)
    section = models.CharField(max_length=10, null=True, blank=True)
    circuit = models.CharField(max_length=10, null=True, blank=True)
    table = models.CharField(max_length=10, null=True, blank=True)
    pdf_path = models.FileField(upload_to=UPLOAD_TO) #TODO: definir bien upload_to
    image = models.ImageField(upload_to=UPLOAD_TO) #TODO: definir bien upload_to

    unique_together = ("section", "circuit", "table")
