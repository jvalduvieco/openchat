from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestPostsRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_can_create_a_new_post(self):
        register_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        })

        registered_user = register_response.get_json()
        response = self.client.post('/users/%s/timeline' % registered_user['id'], json={
            "text": "Hello everyone. I'm Alice."
        })

        json_response = response.get_json()

        self.assertEqual(201, response.status_code)
        self.assertEqual(registered_user['id'], json_response['userId'])
        self.assertIsInstance(json_response['text'], str)
        self.assertIsInstance(json_response['dateTime'], str)
        self.assertTrue(validate_uuid4_string(json_response['postId']))

    def test_can_fetch_user_posts(self):
        register_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        })

        registered_user = register_response.get_json()
        create_post_response = self.client.post('/users/%s/timeline' % registered_user['id'], json={
            "text": "Hello everyone. I'm Alice."
        })

        create_post_json_response = create_post_response.get_json()

        fetch_post_response = self.client.get('/users/%s/timeline' % registered_user['id'])

        fetch_post_json_response = fetch_post_response.get_json()
        self.assertEqual(201, register_response.status_code)
        self.assertEqual(201, create_post_response.status_code)
        self.assertEqual(200, fetch_post_response.status_code)

        self.assertEqual(1, len(fetch_post_json_response))
        self.assertEqual(create_post_json_response['postId'], fetch_post_json_response[0]['postId'])
        self.assertEqual(create_post_json_response['text'], fetch_post_json_response[0]['text'])
        self.assertEqual(create_post_json_response['dateTime'], fetch_post_json_response[0]['dateTime'])
