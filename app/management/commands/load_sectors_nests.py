from django.core.management.base import BaseCommand
from django.db import transaction
from app.models import Sector, Nest


class Command(BaseCommand):
    """
    Import Sectors and Nests to db.

    Example:

        manage.py load_sectors
    """

    help = __doc__

    @transaction.atomic
    def handle(self, *args, **options):

        sectors = ['Whānau','Hapū', 'Koromatua Hapū', 'Iwi', 'Tātou']

        koromatuaHapu = ['Ngāti Hurungaterangi', 'Ngāti Pukaki', 'Ngāti Rangiiwaho', 'Ngāti Taeotu', 'Ngāti Te Rorooterangi', 'Ngāti Tunohopu' ]
        iwi = ['Ngāti Whakaue']
        tatou = ['Tātou']

        try:
            for k in sectors:
                Sector.objects.create(name=k)

            print('The Sector table was filled up.')

            koromatuaHapuSector = Sector.objects.get(name='Koromatua Hapū')
            for k in koromatuaHapu:
                Nest.objects.create(name=k, kinship_sector=koromatuaHapuSector)

            IwiSector = Sector.objects.get(name='Iwi')
            for k in iwi:
                Nest.objects.create(name=k, kinship_sector=IwiSector)

            TatouSector = Sector.objects.get(name='Tātou')
            for k in tatou:
                Nest.objects.create(name=k, kinship_sector=TatouSector)

            print('The Nest table was filled up.')

        except Exception as e:
            transaction.set_rollback(True)
            print("Failed to add Sector or Nest with error: {}".format(e))
