import os
from unittest import TestCase
from unittest.mock import patch

from apps.RESTAPI.__main__ import main


@patch('apps.RESTAPI.__main__.create_openchat_app')
class TestLoginRequests(TestCase):
    def test_can_login_a_user(self, mock_method):
        os.environ['LISTEN'] = '6.6.6.6'
        os.environ['PORT'] = '1337'
        os.environ['ENV'] = 'test'

        main()

        print(mock_method.call_args_list)
        assert mock_method.called
        assert len(mock_method.call_args_list) == 1
        assert mock_method.call_args_list[0][1] == {'config': {'SERVER_NAME': '6.6.6.6:1337'}, 'environment': 'test'}
