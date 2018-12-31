import json
from unittest import TestCase

from apps.RESTAPI.__main__ import create_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestRegistrationRequests(TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_can_authenticate(self):
        response = self.client.post('/registration', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }"""))

        json_response = json.loads(response.get_data(as_text=True))

        assert "Alice" == json_response['username']
        assert "I love playing the piano and travelling." == json_response['about']
        assert "alki324d" == json_response['password']
        assert validate_uuid4_string(json_response['id']) is True
