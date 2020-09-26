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
            'culturalnarratives':{'eng':'Cultural narratives','mao':'Ngā kōrero tuku iho'},
            'welcome':{'eng':'Kia ora','mao':'Kia ora'},
            'toolmanager':{'eng':'Tool manager','mao':'Whakahaere utauta'},
            'gotomap':{'eng':'Go To Map','mao':'Haere ki te'},
            'layers':{'eng':'Layers','mao':'Apaapa'},
            'uploadlayer':{'eng':'Upload Layer','mao':'Tuku atu te apaapa'},
            'mylayers':{'eng':'My Layers','mao':'Aku apaapa'},
            'layeroptions':{'eng':'Layer Options','mao':'Kōwhiringa apaapa'},
            'zoomtolayer':{'eng':'Zoom to layer','mao':'Whakatata atu ki te apaapa'},
            'renamelayer':{'eng':'Rename layer','mao':'Ingoa apaapa'},
            'editlayer':{'eng':'Edit layer','mao':'Whakarerekētia te apaapa'},
            'addcopyright':{'eng':'Add copyright','mao':'Tāpirihia te manatārua'},
            'editcopyright':{'eng':'Edit copyright','mao':'Whakarerekētia te manatārua'},
            'editstyle':{'eng':'Edit style','mao':'Tōrire whakatika'},
            'layerstyle':{'eng':'Layer style','mao':'Tōrire apaapa'},
            'sharelayer':{'eng':'Share layer','mao':'Toha apaapa'},
            'deletelayer':{'eng':'Delete layer','mao':'Whakakore apaapa'},
            'map': {'eng':'Map','mao':'Mahere'},
            'externallayers': {'eng':'External layers','mao':'Apaapa ā-waho'},
            'internallayers': {'eng':'Internal layers','mao':'Apaapa ā-roto'},
            'addnewnarrative': {'eng':'Add new narrative','mao':'Tāpiri kōrero hou'},
            'narratives': {'eng':'Narratives','mao':'He kōrero'},
            'mynarratives': {'eng':'My narratives','mao':'Aku korero'},
            'othernarratives': {'eng':'Other narratives','mao':'Korero whanui'},
            'publicnarratives': {'eng':'Public narratives','mao':'Kōrero tūmatanui'},
            'searchnarratives': {'eng':'Search narratives','mao':'Rapu kōrero'},
            'usermanual': {'eng':'User manual','mao':'Puka aratohu'},
            'about': {'eng':'About','mao':'He whakamārama'},
            'moreinfo': {'eng':'More info','mao':'He kōrero anō'},
            'otherdatasources': {'eng':'Other data sources','mao':'He puna kōrero anō'},
            'logout': {'eng':'Logout','mao':'Takiputa'},
            'login': {'eng':'Login','mao':'Takiuru'},
            'createaccount': {'eng':'Create account','mao':'Hanga taunga'},
            'forgotyourpassword': {'eng':'Forgot your password?','mao':'Kua wareware i a koe tō kupuhuna?'},
            'delete': {'eng':'Delete','mao':'Muku'},
            'cancel': {'eng':'Cancel','mao':'Whakakore'},
            'close': {'eng':'Close','mao':'Katia'},
            'save': {'eng':'Save','mao':'Puritia'},
            'title': {'eng':'Title','mao':'Taitara'},
            'date': {'eng':'Date','mao':'Te rā'},
            'typeofnarrative': {'eng':'Type of narrative','mao':'Momo kōrero'},
            'god': {'eng':'God','mao':'Atua'},
            'summary': {'eng':'Summary','mao':'Whakarāpopototanga'},
            'addelementtostory': {'eng':'Add element to story','mao':'Tāpiri āhuatanga hōu'},
            'newtextfield': {'eng':'New text field','mao':'Tuhinga hōu'},
            'uploadmediafile': {'eng':'Upload media file','mao':'Tuku konae'},
            'drawshape': {'eng':'Draw location','mao':'Tā āhua'},
            'reuseshape': {'eng':'Reuse location','mao':'Whakamahi āhua anō'},
            'scrolltop': {'eng':'Scroll top','mao':'Panuku'},
            'uploadfile': {'eng':'Upload file (video/audio/image)','mao':'Tuku kōnae atu (whakaataata/oro/whakaahua)'},
            'gotit': {'eng':'Got it!','mao':'Kua mau!'},
            'add': {'eng':'Add','mao':'Tāpiri'},
            'editstory': {'eng':'Edit story','mao':'Tõrire kōrero'},
            'print': {'eng':'Print','mao':'Tāhia'},
            'comments': {'eng':'Comments','mao':'Pito kōrero'},
            'cocreatenarrative': {'eng':'Co-create narrative','mao':'Hanga whare kōrero'},
            'submitnarrative': {'eng':'Submit narrative','mao':'Tuku kōrero'},
            'unpublishnarrative': {'eng':'unpublishnarrative','mao':'Tāhia'},
            'viewnarrative': {'eng':'view narrative','mao':'Tirohia te kōrero'},
            'deletenarrative': {'eng':'delete narrative','mao':'Whakakorea te kōrero'},
            'savestory': {'eng':'Save story','mao':'Tiakina te kōrero'},
            'storyfeatureinfo': {'eng':'Story feature info','mao':'He pito Kōrero'},
            'name': {'eng':'Name','mao':'Ingoa'},
            'description': {'eng':'Description','mao':'Whakaaturanga'},
            'addshapetostory': {'eng':'Add shape to story','mao':'Whakauru āhua'},
            'attention': {'eng':'Attention','mao':'Aro mai'},
            'yes': {'eng':'Yes','mao':'Āe'},
            'no': {'eng':'No','mao':'Kao'},
            'dragme': {'eng':'Drag me','mao':'Tōia mai'},
            'updatestory': {'eng':'Update story','mao':'Whakahou te kōrero'},
            'search': {'eng':'Search','mao':'Rapu'},
            'opennarrative': {'eng':'Open narrative','mao':'Huakina te kōrero'},
            'accept': {'eng':'Accept','mao':'Whakaaetia'},
            'review': {'eng':'Review','mao':'Tātari'},
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

        # by Atua	ā-atua
        # by Type of narrative	Ā-kōrero
        # My profile	Ko au
        # Whānau page	Whārangi whānau
        # Nests settings page
        # Users settings page
        # Help	Āwhina
        # Look & Feel
        # First name(s)	Ingoa tuatara
        # Last name(s)	Ingoa whānau
        # Bio	Haurongo
        # Date of birth	Rā whānau
        # Edit profile
        # Request access to wider nests	He tono
        # Change picture	Tīni Whakaahua
        # Save picture	Tiaki whakaahua
        # Phone number	Nama waea
        # My Whānau groups	Aku rōpū whānau
        # Pending invitations	Ngā pōhiri tārewa tonu
        # New	Hōu
        # Invite member	He pōhiri mema
        # Send invite	Tuku pōhiri
        # Accept	Whakaaetia
        # Reject	Whakarerea
        # Nests settings 	Ngā whakataunga kohanga
        # Add new nest	Tāpirihia he kohanga hou
        # Unit/Sector/Level
        # Users settings	Puka
        # Edit	Whakarereke
        # Affiliation	Hononga
        # Themes	Kaupapa
