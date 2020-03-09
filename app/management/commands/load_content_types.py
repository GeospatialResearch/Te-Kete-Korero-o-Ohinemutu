from django.core.management.base import BaseCommand
from app.models import ContentType


class Command(BaseCommand):
    """
    Import ContentType to db.

    Example:

        manage.py load_content_type
    """

    help = __doc__

    def handle(self, *args, **options):

        contentTypeObj = ['Waiata','Pepeha','Whakatauki','Pūrākau','Mōteatea','Mahitoi']

        try:
            for k in contentTypeObj:
                ContentType.objects.create(type=k)

            print('The ContentType table was filled up.')

        except Exception as e:
            print("Failed to create add ContentType with error: {}".format(e))
