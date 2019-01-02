import json
from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestRegistrationRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_can_fetch_a_registered_user(self):
        register_response = self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }"""))

        register_json_response = json.loads(register_response.get_data(as_text=True))

        query_user_response = self.client.get('/users/%s' % register_json_response['id'])
        query_user_json_response = json.loads(register_response.get_data(as_text=True))

        assert 200 == query_user_response.status_code
        assert "Alice" == query_user_json_response['username']
        assert "I love playing the piano and travelling." == query_user_json_response['about']
        assert "alki324d" == query_user_json_response['password']
        assert register_json_response['id'] == query_user_json_response['id']
        assert validate_uuid4_string(query_user_json_response['id']) is True

    def test_can_fetch_all_users(self):
        self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }"""))
        register_response = self.client.post('/users', json=json.loads("""{
            "username" : "Maria",
            "password" : "27398273",
            "about" : "I love playing the chess and dancing."
        }"""))

        json.loads(register_response.get_data(as_text=True))

        query_user_response = self.client.get('/users')
        query_user_json_response = json.loads(query_user_response.get_data(as_text=True))

        assert 200 == query_user_response.status_code
        assert len(query_user_json_response) == 2
