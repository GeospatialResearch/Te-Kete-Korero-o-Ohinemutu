from django.core.management.base import BaseCommand
from app.models import WebsiteTranslation
import argparse

class Command(BaseCommand):
    """
    Import translations to db.

    Example:

        manage.py load_website_translations --ignoredb yes
    """

    help = __doc__

    def add_arguments(self, parser):
        parser.formatter_class = argparse.RawDescriptionHelpFormatter
        parser.add_argument(
            '--ignoredb', required=True, metavar='IGNOREDB',
            help=('Whether should ignore the data in the WebsiteTranslation table'))

    def handle(self, *args, **options):

        ignoredb = options['ignoredb']

        langObj = {
            'map': {'eng':'Map','mao':'Mahere'},
            'myLayers': {'eng':'My layers','mao':'Papa'},
            'extLayers': {'eng':'External layers','mao':'Papanga o waho'},
            'addNewNarrative': {'eng':'Add new narrative','mao':'Tāpirihia he korero hou'},
            'myNarratives': {'eng':'My narratives','mao':'Aku korero'},
            'otherNarratives': {'eng':'Other narratives','mao':'Korero whanui'},
            'general':{'eng':'General','mao':'Whānui'},
            'culturalNarratives':{'eng':'Cultural narratives','mao':'Kōrero tuku iho'},
            'uploadDataset': {'eng':'Upload Layer','mao':'Tuku i te toharite'},
            'search': {'eng':'Search','mao':'Rapunga'}
        }

        try:
            dbTranslations = WebsiteTranslation.objects.all()

            if ignoredb ==  'yes':
                WebsiteTranslation.objects.all().delete()
                for k in langObj:
                    WebsiteTranslation.objects.create(
                        field_name=k,
                        eng=langObj[k]['eng'],
                        mao=langObj[k]['mao'])
                print('The WebsiteTranslation table was filled up.')

            else:
                ready = True
                for dbt in dbTranslations:
                    if dbt.eng != langObj[dbt.field_name]['eng']:
                        print("The english value of the field {} in the WebsiteTranslation table is different in the langObj".format(dbt.field_name))
                        ready = False
                    if dbt.mao != langObj[dbt.field_name]['mao']:
                        print("The maori value of the field {} in the WebsiteTranslation table is different in the langObj".format(dbt.field_name))
                        ready = False

                if ready:
                    print('The values of the records existing in the WebsiteTranslation table match the langObj. Ready to override.')

        except Exception as e:
            print("Failed to create translations with error: {}".format(e))
