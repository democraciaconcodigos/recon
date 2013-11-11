# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

UPLOAD_TO = settings.TELEGRAMA_MEDIA_ROOT

class Telegram(models.Model):
    section = models.CharField(max_length=10)
    circuit = models.CharField(max_length=10)
    table = models.CharField(max_length=10)
    province = models.CharField(max_length=15, default="Córdoba")
    pdf = models.FileField(upload_to=UPLOAD_TO) #TODO: definir bien upload_to
    image = models.ImageField(upload_to=UPLOAD_TO, null=True, blank=True) #TODO: definir bien upload_to
    tables = models.ForeignKey("Table")

    unique_together = ("section", "circuit", "table")
    
    # @classmethod
    # def cells(self):
    # 	return Cells.objects.filter()

    def get_image_url(self):
    	pass

	def __unicode__(self):
		return self.id


class Table(models.Model):
	name = models.CharField(max_length=50)
	cells = models.ForeignKey("Cell")

	def __unicode__(self):
		return self.name


class Cell(models.Model):
    position = models.CharField(max_length=10)
    name = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to=UPLOAD_TO)
    data = models.CharField(max_length=50)
    score = models.DecimalField(max_digits=4, decimal_places=3)

    def __unicode__(self):
        return self.name if self.name else self.position
