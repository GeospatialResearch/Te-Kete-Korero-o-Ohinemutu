#!/usr/bin/env python3

class Command(BaseCommand):
    help = 'Loads test data'

    def handle(self, *args, **options):
        # Let's make sure we don't do this in prod!
        try:
            User.objects.create_superuser('admin@example.com', 'password')
        except Exception as e:
            print("Failed to create super user with error: {}".format(e))
