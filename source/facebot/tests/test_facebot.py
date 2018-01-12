from facebot.facebot import FaceBot
import pytest

from unittest.mock import call


@pytest.fixture()
def mock_fb_api(mocker):
    mock_graph = mocker.patch('facebook.GraphAPI')
    mocker.patch.object(FaceBot, 'find_fb_id', return_value=1234567890)

    return mock_graph


@pytest.mark.usefixtures('mock_fb_api')
class TestFaceBot:

    def test_init_fills_missing_id_with_url(self):
        fb = FaceBot(url='https://facebook.com/google')

        fb.find_fb_id.assert_called_once_with('https://facebook.com/google')
        assert fb.page_id == 1234567890

    def test_init_fills_missing_id_with_page_name(self, mock_fb_api):
        mock_fb_api.return_value.get_object.return_value = {'id': 9876543210}
        fb = FaceBot(page_name='Google')

        assert fb.graph.get_object.called_once_with(fb.page_name)
        assert fb.page_id == 9876543210

    def test_init_fills_missing_page_name(self, mock_fb_api):
        mock_fb_api.return_value.get_object.return_value = {'name': 'Google'}
        fb = FaceBot(url='https://google.com')

        assert fb.graph.get_object.called_once_with(fb.page_id)
        assert fb.page_name == 'Google'

    def test_init_fills_missing_url(self, mock_fb_api):
        mock_fb_api.return_value.get_object.return_value = {'id': 9876543210,
                                                            'link': 'https://facebook.com/google'}
        fb = FaceBot(page_name='Google')

        assert fb.graph.get_object.called_once_with(fb.page_id)
        assert fb.url == 'https://facebook.com/google'

    def test_init_raises_exception_when_no_parameters_input(self):
        with pytest.raises(TypeError):
            FaceBot()

    def test_get_posts_appends_date_parameter_to_graph_kwargs(self):
        fb = FaceBot(url='https://facebook.com/google')
        fb.get_posts(date='1999-12-31')

        fb.graph.get_all_connections.has_calls(call(since='1999-12-31'), any_order=True)

    def test_get_posts_raises_exception_if_date_parameter_wrong_format(self):
        with pytest.raises(ValueError):
            fb = FaceBot(url='https://facebook.com/google')
            fb.get_posts(date='31-12-1999')

    def test_get_photos_appends_date_parameter_to_graph_kwargs(self):
        fb = FaceBot(url='https://facebook.com/google')
        fb.get_photos(date='1999-12-31')

        fb.graph.get_all_connections.has_calls(call(since='1999-12-31'), any_order=True)

    def test_get_photos_raises_exception_if_date_parameter_wrong_format(self):
        with pytest.raises(ValueError):
            fb = FaceBot(url='https://facebook.com/google')
            fb.get_photos(date='31-12-1999')

    def test_get_business_hours_returns_hours_as_dict(self, mock_fb_api):
        mock_fb_api.return_value.get_object.return_value = {
            "hours": {
                "tue_1_open": "07:00",
                "tue_1_close": "21:00",
                "wed_1_open": "07:00",
                "wed_1_close": "21:00",
                "thu_1_open": "07:00",
                "thu_1_close": "21:00",
                "fri_1_open": "07:00",
                "fri_1_close": "21:00",
                "sat_1_open": "07:00",
                "sat_1_close": "21:00"
            }
        }

        hours = {
            'tue': ['07:00', '21:00'],
            'wed': ['07:00', '21:00'],
            'thu': ['07:00', '21:00'],
            'fri': ['07:00', '21:00'],
            'sat': ['07:00', '21:00'],
        }

        fb = FaceBot(url='https://facebook.com/google')

        assert fb.get_business_hours() == hours
