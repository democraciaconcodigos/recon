# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
import os



def upload_location(instance, filename):
    """
    Genera el path para guardar las imágenes de los telegramas y celdas.

    El path es relativo a settings.MEDIA_ROOT
    Estructura: /media_path../telegramas/<provincia>/<sección>_<circuito>_<mesa>/
                [<provincia>_<sección>_<circuito>_<mesa>.{pdf, jpg}, 
                 <nombre_tabla>_<posición_de_celda>.jpg*
                ]
    .jpg
    """
    i = instance
    ext = filename.split('.')[-1]
    name = None
    if isinstance(i, Cell):
        name =  "%s_%s.%s" % (i.table.name, i.position, ext)
        i = i.table.telegram  # Hack feo para reusar código

    p, s, c, t = i.province, i.section, i.circuit, i.table
    dir_path = os.path.join("telegramas", p, "%s_%s_%s" % (s, c, t))
    if not name:
        # Instance es un telegrama
        name =  "%s_%s_%s_%s.%s" % (p, s, c, t, ext)

    return os.path.join(dir_path, name)


class Telegram(models.Model):
    """
    Modelo de un telegrama.

    Cada telegrama es identificable por la 3-upla (section, circuit, table)
    """
    section = models.CharField(max_length=10)
    circuit = models.CharField(max_length=10)
    table = models.CharField(max_length=10)  # Número de mesa (No es una tabla)
    province = models.CharField(max_length=15, default="Córdoba")
    pdf = models.FileField(upload_to=upload_location)
    image = models.ImageField(upload_to=upload_location, null=True, blank=True)

    unique_together = ("section", "circuit", "table")

    def get_image_url(self):
        pass

    def __unicode__(self):
        return "Telegrama (%s, %s, %s)" % (self.section, self.circuit,
                                           self.table)


class Table(models.Model):
    """
    Modelo para las tablas que contiene un telegrama.
    """
    name = models.CharField(max_length=50)
    telegram = models.ForeignKey("Telegram", related_name="tables")

    def __unicode__(self):
        return "%s del %s" % (self.name, self.telegram)


class Cell(models.Model):
    """
    Modelo para las celdas dentro de las tablas de un telegrama.
    """
    position = models.CharField(max_length=10)
    image = models.ImageField(upload_to=upload_location)
    data = models.CharField(max_length=50, null=True, blank=True)
    score = models.DecimalField(max_digits=4, decimal_places=3,
                                null=True, blank=True)
    table = models.ForeignKey("Table", related_name="cells")

    def __unicode__(self):
        return "Celda %s de tabla %s" % (self.position, self.table)
