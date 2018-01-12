import facebook
import requests

from collections import defaultdict
import datetime

import os

TOKEN = os.environ['FB_TOKEN']


class FaceBot:
    """
    Bot to interface with the facebook graph api
    """

    def __init__(self, page_id: int = None, page_name: str = None, url: str = None):
        """
        Takes either a page_id, page_name, or url of a facebook page and fills in the missing values
        Uses v2.11 of the facebook graph api

        Args:
            page_id: The numeric id of a facebook page
            page_name: The string name of a facebook page
            url: The url of a facebook page
        """

        self.graph = facebook.GraphAPI(access_token=TOKEN, version='2.11')
        self.page_id = page_id
        self.page_name = page_name
        self.url = url

        if not page_id and not page_name and not url:
            raise TypeError('Value for either page_id, page_name or url is required')

        # First, get the page id if not filled
        if not page_id:

            if url:
                self.page_id = self.find_fb_id(url)

            elif page_name:
                self.page_id = int(self.graph.get_object(page_name).get('id'))

        if not page_name:
            self.page_name = self.graph.get_object(self.page_id).get('name')

        if not url:
            self.url = self.graph.get_object(self.page_id, fields='link').get('link')

    @staticmethod
    def find_fb_id(url: str):
        """
        Makes an ajax post request to find a facebook page's numeric id

        Args:
            url: The url of the facebook page

        Returns:
            int facebook page id
        """

        r = requests.post('https://findmyfbid.com', data={'url': url})

        return r.json()['id']

    def get_posts(self, date: str = None):
        """
        Gets facebook posts from a facebook page.
        If the date parameter is provided, only fetch posts created since that date.
        Otherwise, fetches all posts.

        Args:
            date: String in the format 'YYYY-MM-DD'

        Returns:
            List of dictionaries.  Each dictionary is a facebook post.
            Posts with multiple images have a nested attachments dictionary.
        """

        kwargs = {
            'id': self.page_id,
            'connection_name': 'posts',
            'fields': 'message,created_time,full_picture,object_id,attachments{subattachments}'
        }

        if date:

            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                kwargs['since'] = date

            except ValueError:
                raise ValueError('Date should be in the format YYYY-MM-DD')

        post_list = self.graph.get_all_connections(**kwargs)
        posts = []

        for p in post_list:
            posts.append(p)

        return posts

    def get_post(self, post_id: str = None):
        post = self.graph.get_object(post_id, fields='message,created_time')

        return post

    def get_photos(self, date: str = None):
        """
        Gets facebook photos from a facebook page.
        If the date parameter is provided, only fetch photos created since that date.
        Otherwise, fetches all photos.

        Args:
            date: String in the format 'YYYY-MM-DD'

        Returns:
            A list of dictionaries.  Each dictionary is a full resolution facebook photo.
        """

        kwargs = {
            'id': self.page_id,
            'connection_name': 'photos',
            'type': 'uploaded',
            'fields': 'images,page_story_id,created_time'
        }

        if date:

            try:
                datetime.datetime.strptime(date, '%Y-%m-%d')
                kwargs['since'] = date

            except ValueError:
                raise ValueError('Date should be in the format YYYY-MM-DD')

        photo_list = self.graph.get_all_connections(**kwargs)
        photos = []

        # parse api return value to only get necessary fields
        for p in photo_list:
            photo_id = p['id']
            photos.append({
                'id': photo_id,
                'page_story_id': p.get('page_story_id'),
                'source': p['images'][0]['source'],
                'created_time': p['created_time']
            })

        return photos

    def get_profile_picture(self):
        profile_picture = self.graph.get_object(id=self.page_id,
                                                fields='picture.width(1000).height(1000)')['picture']['data']['url']

        return profile_picture

    def get_cover_picture(self):
        cover_id = self.graph.get_object(id=self.page_id,
                                         fields='cover')['cover']['id']
        full_cover = self.graph.get_object(id=cover_id, fields='images')['images'][0]['source']

        return full_cover

    def get_phone_number(self):
        phone_number = self.graph.get_object(id=self.page_id, fields='phone').get('phone')

        return phone_number

    def get_business_hours(self):
        """
        Gets the business hours for a facebook page.

        Returns:
            A dictionary with days as keys and a list as the value.  0th element of the list is the opening hour,
            1st element is closing hour
        """

        hours = self.graph.get_object(id=self.page_id, fields='hours').get('hours')

        # jam opening and closing time into a single list
        if hours:
            hours_tuples = [(key, value) for key, value in hours.items()]
            hours_open_close = defaultdict(list)

            for key, value in hours_tuples:
                hours_open_close[key[:3]].append(value)
                hours_open_close[key[:3]].sort()

            return dict(hours_open_close)

        else:
            return None

    def get_about(self):
        about = self.graph.get_object(id=self.page_id, fields='about').get('about')

        return about

    def get_description(self):
        description = self.graph.get_object(id=self.page_id, fields='description').get('description')

        return description

    def get_address(self):
        address = self.graph.get_object(id=self.page_id, fields='single_line_address').get('single_line_address')

        return address
