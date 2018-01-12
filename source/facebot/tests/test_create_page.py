from django.core.management import call_command

from facebot.models import FacePage

import pytest


@pytest.fixture()
def mock_facebot(mocker):
    mock_facebot = mocker.patch('facebot.management.commands.create_page.FaceBot')
    mock_requests = mocker.patch('facebot.management.commands.create_page.requests')

    mock_facebot.return_value.page_id = 1234567890
    mock_facebot.return_value.url = 'https://facebook.com/google'
    mock_facebot.return_value.page_name = 'Google'
    mock_facebot.return_value.get_phone_number.return_value = '0118-999-881-999-119-725-3'
    mock_facebot.return_value.get_about.return_value = 'about'
    mock_facebot.return_value.get_description.return_value = 'description'
    mock_facebot.return_value.get_address.return_value = 'address'
    mock_facebot.return_value.get_business_hours.return_value = {'tue': ['01:00', '23:00']}

    return mock_facebot, mock_requests


@pytest.mark.django_db()
@pytest.mark.usefixtures('mock_facebot')
class TestCreatePage:

    def test_create_page_does_not_create_duplicate_pages(self):
        call_command('create_page', 'https://facebook.com/dfdfdfdf')
        call_command('create_page', 'https://facebook.com/dfdfdfdf')

        assert FacePage.objects.count() == 1
