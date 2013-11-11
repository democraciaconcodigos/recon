# -*- coding: utf-8 -*-
from models import Telegram

def get_telegram_image_url(request, section, circuit, table):
	""" Devuelve url de la imagen completa del telegrama """
	telegram = Telegram.objects.get(section=section, circuit=circuit, table=table)
	return telegram.get_telegram_image_url()


def get_cell_image(request, section, circuit, table, table_id, cell_id):
	""" Devuelve la url de imagen de una celda del telegrama """
	telegram = Telegram.objects.get(section=section, circuit=circuit, table=table)
	telegram.cells.get()


def parse_cell(telegram_id, cell_id):
	"""
	Devuelve lista con los valores reconocidos de la imagen

	El orden de precisión es descendente, osea, el primer valor es el mas probable
	"""


# TODO: usar tastypie en vez