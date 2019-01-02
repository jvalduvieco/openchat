import json
from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestPostsRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_can_create_a_new_post(self):
        register_response = self.client.post('/users', json=json.loads("""{
                "username" : "Alice",
                "password" : "alki324d",
                "about" : "I love playing the piano and travelling."
            }"""))

        registered_user = json.loads(register_response.get_data(as_text=True))
        response = self.client.post('/users/%s/timeline' % registered_user['id'], json=json.loads("""{
            "text" : "Hello everyone. I'm Alice."
        }"""))

        json_response = json.loads(response.get_data(as_text=True))

        assert 201 == response.status_code
        assert registered_user['id'] == json_response['userId']
        assert type(json_response['text']) is str
        assert type(json_response['dateTime']) is str
        assert validate_uuid4_string(json_response['postId'])

    def test_can_fetch_user_posts(self):
        register_response = self.client.post('/users', json=json.loads("""{
                "username" : "Alice",
                "password" : "alki324d",
                "about" : "I love playing the piano and travelling."
            }"""))

        registered_user = json.loads(register_response.get_data(as_text=True))
        create_post_response = self.client.post('/users/%s/timeline' % registered_user['id'], json=json.loads("""{
            "text" : "Hello everyone. I'm Alice."
        }"""))

        create_post_json_response = json.loads(create_post_response.get_data(as_text=True))

        fetch_post_response = self.client.get('/users/%s/timeline' % registered_user['id'])

        fetch_post_json_response = json.loads(fetch_post_response.get_data(as_text=True))

        assert 201 == register_response.status_code
        assert 201 == create_post_response.status_code
        assert 200 == fetch_post_response.status_code

        assert 1 == len(fetch_post_json_response)
        assert create_post_json_response['postId'] == fetch_post_json_response[0]['postId']
        assert create_post_json_response['text'] == fetch_post_json_response[0]['text']
        assert create_post_json_response['dateTime'] == fetch_post_json_response[0]['dateTime']
