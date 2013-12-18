# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.core import serializers
from django.utils import simplejson

from models import Telegram


def get_telegram_image_url(request, section, circuit, mesa):
	""" Devuelve url de la imagen completa del telegrama """
	telegram = Telegram.objects.get(section=section, circuit=circuit, mesa=mesa)
	return telegram.get_telegram_image_url()


def get_cell_image(request, section, circuit, mesa, table_id, cell_id):
	""" Devuelve la url de imagen de una celda del telegrama """
	telegram = Telegram.objects.get(section=section, circuit=circuit, mesa=mesa)
	telegram.cells.get()


def parse_cell(telegram_id, cell_id):
	"""
	Devuelve lista con los valores reconocidos de la imagen
	El orden de precisión es descendente, osea, el primer valor es el mas probable
	"""

def telegram_detail(request, section, circuit=None, mesa=None):
    """Segun el descripor unico seccion-circuito-mesa obtener el telegrama 
    correspondiente serializado a json.
    Si falta mesa o mesa y circuit devuelve los listados correspondientes.
    """
    telegrams = Telegram.objects.filter(section=section)
    if circuit:
        telegrams = telegrams.filter(circuit=circuit)
    if mesa:
        telegrams = telegrams.filter(mesa=mesa)

    telegrams = list(telegrams.values('id', 'district', 'section', 'circuit', 'mesa', 'province', 'pdf', 'image'))
    jsondata = simplejson.dumps(telegrams)
    #jsondata = serializers.serialize('json', telegrams)
    return HttpResponse(jsondata, mimetype='application/json')


def telegram_cell(request, section, circuit, mesa, tables, cell):
    """Segun el descripor unico seccion-circuito-mesa nombre de tabla y coordenadas obtener la celda 
    correspondiente serializado a json.
    """
    telegrams = Telegram.objects.filter(section=section, circuit=circuit, mesa=mesa)
    telegrams = telegrams.filter(tables__name=tables, tables__cells__position=cell)
    jsondata = serializers.serialize('json', telegrams)

    return HttpResponse(jsondata, mimetype='application/json')



