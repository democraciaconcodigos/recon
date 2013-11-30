#coding=utf-8
from django.core.management.base import BaseCommand, CommandError
from telegrama.models import Telegram, Cell  # , Table


def parse_spot_from_telegram():
    """ Returns a tuple (parsed_data, parsed_score) being those the data read
        from the OCR and the credibility score (a value between 0 and 1)
    """
    # llama a digit.algo y procesa
    # pseudocode!!!
    return True


class Command(BaseCommand):
    """ Process telegrams reading (ocr) from the telegrams given all the
        fields and saving each obtained value (and score) in the DB.
    """

    args = '<telegrama_id telegrama_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        # pseudocode, pseudocode everywhere!!!

        # get telegrams to process
        teleg_tables = Telegram.objects.all()

        # las coordenadas desde donde sacar los datos?
        #     podrían estar en la DB y ser administradas desde admin, para
        #     poder aplicar a otra clase de telegramas (incluso a extenderlo
        #     a cualquier clase de documento)
        data_spots = 'dummy_string_assignation_to_change!!!'

        if args:
            # armar lista de IDs
            id_list = args.to_list()  # FIXME!!!!!

            # agarrar ese|esos telegrama(s)
            teleg_tables = teleg_tables.filter(id__in=id_list)

        for tt in teleg_tables:
            for spot in data_spots:
                try:
                    # image = ¿¿??
                    # table = ¿¿??
                    parsed_data, parsed_score = parse_spot_from_telegram(tt,
                                                                         spot)
                    newCell = Cell(data=parsed_data,
                                   score=parsed_score,
                                   #table=¿¿??,
                                   #image=¿¿??,
                                   #position=¿¿??
                                   )
                    newCell.save()

                except:
                    raise CommandError('Se clavó procesando el telegrama "%s"'
                                       % tt)

        print("Terminaron de procesarse los telegramas.")
