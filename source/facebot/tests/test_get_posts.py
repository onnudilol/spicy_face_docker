from django.core.management import call_command
from django.core.exceptions import ObjectDoesNotExist

from facebot.models import FacePage, PagePost

import pytest


@pytest.fixture()
def mock_facebot(mocker):
    mock_facebot = mocker.patch('facebot.management.commands.get_posts.FaceBot')
    mock_requests = mocker.patch('facebot.management.commands.get_posts.requests')

    mock_facebot.get_posts.return_value = [{'message': 'hello', 'created_time': '2018-01-10T22:20:00+0000',
                                            'object_id': '1761844897200437', 'id': '169299103121699_1761844897200437',
                                            'full_picture': 'https://example.com/example.jpg'}]

    return mock_facebot, mock_requests


@pytest.fixture()
def face_page():
    return FacePage.objects.create(page_id=1234567890, url='https://facebook.com/google', page_name='Google')


@pytest.mark.django_db()
@pytest.mark.usefixtures('mock_facebot')
class TestCreatePage:

    def test_get_posts_raises_error_if_no_page_exists(self):
        with pytest.raises(ObjectDoesNotExist):
            call_command('get_posts')

    def test_get_posts_raises_error_if_date_argument_is_wrong_format(self, face_page):
        with pytest.raises(ValueError):
            call_command('get_posts', date='12-31-1999')

    def test_get_posts_gets_all_posts_if_no_arguments(self, mock_facebot, face_page):
        call_command('get_posts')

        assert mock_facebot[0].get_posts.call_args is None

    def test_get_posts_does_not_create_images_if_post_already_exists(self, mock_facebot, face_page):
        PagePost.objects.create(page_post_id='169299103121699_1761844897200437',
                                created_time='2018-01-10T22:20:00+0000')
        call_command('get_posts')

        assert mock_facebot[1].get.call_args is None
