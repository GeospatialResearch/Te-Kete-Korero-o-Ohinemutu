from django.core.management.base import BaseCommand
from app.models import Atua


class Command(BaseCommand):
    """
    Import atuas to db.

    Example:

        manage.py load_atua
    """

    help = __doc__

    def handle(self, *args, **options):

        atuaObj = ['Tāne','Tangaroa','Tāwhirimātea', 'Tūmatauenga', 'Rongomātāne','Haumietiketike','Rūaumoko']

        try:
            for k in atuaObj:
                Atua.objects.create(name=k)

            print('The Atua table was filled up.')

        except Exception as e:
            print("Failed to create add atua with error: {}".format(e))
