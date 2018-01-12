from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.db import IntegrityError

from facebot.models import FacePage, PagePost, TimelineImage
from facebot.facebot import FaceBot

import requests

import datetime


class Command(BaseCommand):
    help = 'Gets posts from a facebook page.'

    def add_arguments(self, parser):
        parser.add_argument('-d', '--date', type=str, required=False, help='Date in YYYY-MM-DD format')
        parser.add_argument('-l', '--latest', action='store_true', help='Get latest posts since last update.')

    def handle(self, *args, **options):

        try:
            page = FacePage.objects.first()
            fb = FaceBot(page.page_id)

        except AttributeError:
            raise ObjectDoesNotExist('No facebook pages found.  Run the create_page command first.')

        if options['date']:

            try:
                datetime.datetime.strptime(options['date'], '%Y-%m-%d')
                posts = fb.get_posts(options['date'])

            except ValueError:
                raise ValueError('Date should be in the format YYYY-MM-DD')

        elif options['latest']:
            latest_date = PagePost.objects.latest('created_time')
            posts = fb.get_posts(latest_date)

        else:
            posts = fb.get_posts()

        for post in posts:

            page_post, created = PagePost.objects.get_or_create(
                page_post_id=post['id'],
                defaults={'created_time': post['created_time'], 'message': post.get('message')}
            )

            if created:

                if post.get('full_picture'):
                    r = requests.get(post['full_picture'])

                    if r.status_code == requests.codes.ok:
                        img_content = ContentFile(r.content)

                        full_img_id = post.get('object_id', post['id'].split('_')[1])
                        image = TimelineImage(post=page_post, timeline_image_id=full_img_id,
                                              created_time=post['created_time'])
                        image.image.save(f'{full_img_id}_full.jpg', img_content)
                        image.save()

                if post.get('attachments'):
                    subattachments = post['attachments']['data'][0]['subattachments']['data']

                    for attachment in subattachments:

                        if attachment['type'] == 'photo':
                            r = requests.get(attachment['media']['image']['src'])

                            if r.status_code == requests.codes.ok:
                                img_content = ContentFile(r.content)
                                image_id = attachment['target']['id']
                                full_img_id = post.get('object_id', post['id'].split('_')[1])

                                # Only create a new image if the image id is distinct from the full picture id
                                if image_id != full_img_id:
                                    image = TimelineImage.objects.create(post=page_post,
                                                                         timeline_image_id=image_id,
                                                                         created_time=post['created_time'])
                                    image.image.save(f'{attachment["target"]["id"]}.jpg', img_content)
                                    image.save()
