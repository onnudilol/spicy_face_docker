from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile

from facebot.models import FacePage
from facebot.facebot import FaceBot

import requests


class Command(BaseCommand):
    help = 'Creates an entry for a facebook page.'

    def add_arguments(self, parser):
        parser.add_argument('url', type=str, help='The url of the facebook page')

    def handle(self, *args, **options):
        page_id = FaceBot.find_fb_id(options['url'])
        fb = FaceBot(page_id=page_id)

        page_info = {
            'page_id': fb.page_id,
            'url': fb.url,
            'page_name': fb.page_name,
            'phone_number': fb.get_phone_number(),
            'about': fb.get_about(),
            'description': fb.get_description(),
            'address': fb.get_address(),
            'hours': fb.get_business_hours(),
        }

        page, created = FacePage.objects.get_or_create(page_id=fb.page_id, defaults=page_info)

        if created:

            # Save profile pic
            r = requests.get(fb.get_profile_picture())

            if r.status_code == requests.codes.ok and not r.headers.get('x-error'):
                page.profile_picture.save(name='profile.jpg', content=ContentFile(r.content))

            # Save cover pic
            r = requests.get(fb.get_cover_picture())

            if r.status_code == requests.codes.ok and not r.headers.get('x-error'):
                page.cover_picture.save(name='cover.jpg', content=ContentFile(r.content))

            page.save()
            self.stdout.write(f'Page {fb.page_name} created.')

        else:
            self.stdout.write(f'Page {fb.page_name} already exists.')
