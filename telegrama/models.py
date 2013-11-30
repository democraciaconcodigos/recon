# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models

UPLOAD_TO = settings.TELEGRAMA_MEDIA_ROOT


class Telegram(models.Model):
    """ Telegram class info
    """
    section = models.CharField(max_length=10)
    circuit = models.CharField(max_length=10)
    table = models.CharField(max_length=10)
    province = models.CharField(max_length=15, default="Córdoba")
    pdf = models.FileField(upload_to=UPLOAD_TO)
    image = models.ImageField(upload_to=UPLOAD_TO, null=True, blank=True)

    unique_together = ("section", "circuit", "table")

    def get_image_url(self):
        pass

    def __unicode__(self):
        return "Telegrama (%s, %s, %s)" % (self.section, self.circuit,
                                           self.table)


class Table(models.Model):
    """ Table class info
    """
    name = models.CharField(max_length=50)
    telegram = models.ForeignKey("Telegram", related_name="tables")

    def __unicode__(self):
        return "%s del %s" % (self.name, self.telegram)


class Cell(models.Model):
    """ Cell class info
    """
    position = models.CharField(max_length=10)
    image = models.ImageField(upload_to=UPLOAD_TO)
    data = models.CharField(max_length=50, null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=3,
                                null=True, blank=True)
    table = models.ForeignKey("Table", related_name="cells")

    def __unicode__(self):
        return "Celda %s de tabla %s" % (self.position, self.table)
