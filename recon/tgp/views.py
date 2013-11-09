from models import Telegram

def get_telegram_image(request, telegram_id):
	""" Devuelve la imagen completa del telegrama """
	try:
		result = Telegram.objects.get(pk=telegram_id)
	except Telegram.DoesNotExist():
		result = None
	return result


def get_cell_image(telegram_id, cell_id):
	""" Devuelve la imagen de una celda del telegrama """
	#TODO: implementar


def parse_cell(telegram_id, cell_id):
	"""
	Devuelve lista con los valores reconocidos de la imagen

	El orden de precisión es descendente, osea, el primer valor es el mas probable
	"""


