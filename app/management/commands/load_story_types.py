from django.core.management.base import BaseCommand
from app.models import StoryType


class Command(BaseCommand):
    """
    Import storytype to db.

    Example:

        manage.py load_story_type
    """

    help = __doc__

    def handle(self, *args, **options):

        storyTypeObj = ['Traditional Narrative','Planning Narrative', 'Treaty narrative', 'Lived Experience', 'Historical Narrative', 'Scientific Narrative']

        try:
            for k in storyTypeObj:
                StoryType.objects.create(type=k,description=k)

            print('The StoryType table was filled up.')

        except Exception as e:
            print("Failed to create add StoryType with error: {}".format(e))
