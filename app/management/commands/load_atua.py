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

        atuaObj = {'Ranginui','Papatūānuku','Tūmatauenga','Tāwhirimātea','Tāne-mahuta','Tangaroa','Rongo','Punga','Haumia-tiketike','Urutengangana','Ruaumoko','Hine-nui-te-pō','Kaitangata','Ikatere','Tū-te-wehiwehi','Māui'}

        try:
            for k in atuaObj:
                Atua.objects.create(name=k)
        except Exception as e:
            print("Failed to create add atua with error: {}".format(e))
