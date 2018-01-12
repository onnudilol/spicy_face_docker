from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.db.utils import IntegrityError

from facebot.models import FacePage, PagePost, TimelineImage
from facebot.facebot import FaceBot

import requests

import datetime


class Command(BaseCommand):
    help = 'Gets photos from a facebook page'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--date', type=str, required=False, help='Date in YYYY-MM-DD format')
        parser.add_argument('-l', '--latest', action='store_true', help='Get latest photos since last update.')

    def handle(self, *args, **options):

        try:
            page = FacePage.objects.first()
            fb = FaceBot(page.page_id)

        except AttributeError:
            raise ObjectDoesNotExist('No facebook pages found.  Run the create_page command first.')

        if options['date']:

            try:
                datetime.datetime.strptime(options['date'], '%Y-%m-%d')
                photos = fb.get_photos(options['date'])

            except ValueError:
                raise ValueError('Date should be in the format YYYY-MM-DD')

        elif options['latest']:
            latest_date = TimelineImage.objects.latest('created_time')
            photos = fb.get_photos(latest_date)

        else:
            photos = fb.get_photos()

        for photo in photos:
            image = TimelineImage(timeline_image_id=photo['id'], created_time=photo['created_time'])

            r = requests.get(photo['source'])

            if r.status_code == requests.codes.ok and not r.headers.get('x-error'):
                img_content = ContentFile(r.content)

                try:
                    image.image.save(name=f'{photo["id"]}.jpg', content=img_content)

                except IntegrityError:
                    pass

            post = None

            if photo['page_story_id']:

                try:
                    post = PagePost.objects.get(page_post_id=str(photo['page_story_id']))

                except PagePost.DoesNotExist:
                    post_info = fb.get_post(photo['page_story_id'])
                    post_info['page_post_id'] = post_info.pop('id')
                    post = PagePost.objects.create(**post_info)

            image.post = post

            try:
                image.save()

            except IntegrityError:
                pass
