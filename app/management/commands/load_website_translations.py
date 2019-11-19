from django.core.management.base import BaseCommand
from app.models import WebsiteTranslation


class Command(BaseCommand):
    """
    Import translations to db.

    Example:

        manage.py load_website_translations
    """

    help = __doc__

    def handle(self, *args, **options):

        langObj = {
            'map': {'eng':'Map','mao':'Mahere'},
            'myLayers': {'eng':'My layers','mao':'Papa'},
            'extLayers': {'eng':'External layers','mao':'papanga o waho'},
            'addNewNarrative': {'eng':'Add new narrative','mao':'Tāpirihia he korero hou'},
            'myNarratives': {'eng':'My Narratives','mao':'Aku korero'},
            'general':{'eng':'General','mao':'Whānui'},
            'culturalNarratives':{'eng':'Cultural narratives','mao':'Kōrero tuku iho'},
            'uploadDataset': {'eng':'Upload dataset','mao':'Tuku i te toharite'},
            'search': {'eng':'Search','mao':'Rapunga'}
        }

        try:
            for k in langObj:
                WebsiteTranslation.objects.create(
                    field_name=k,
                    eng=langObj[k]['eng'],
                    mao=langObj[k]['mao'])
        except Exception as e:
            print("Failed to create add traslations with error: {}".format(e))
