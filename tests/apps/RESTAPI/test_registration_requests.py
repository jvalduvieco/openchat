import json
from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestRegistrationRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_can_register_a_user(self):
        response = self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }"""))

        json_response = json.loads(response.get_data(as_text=True))

        assert 201 == response.status_code
        assert "Alice" == json_response['username']
        assert "I love playing the piano and travelling." == json_response['about']
        assert validate_uuid4_string(json_response['id']) is True

    def test_register_user_bad_parameters_results_in_bad_request(self):
        response = self.client.post('/users', json=json.loads("""{}"""))

        json_response = json.loads(response.get_data(as_text=True))

        assert 400 == response.status_code
        assert json_response['application_error'] is not None
        assert json_response['application_error']['status_code'] == 400
