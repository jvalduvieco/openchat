from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app
from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestRegistrationRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_can_fetch_a_registered_user(self):
        register_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        })

        register_json_response = register_response.get_json()

        query_user_response = self.client.get('/users/%s' % register_json_response['id'])
        query_user_json_response = register_response.get_json()

        self.assertEqual(200, query_user_response.status_code)
        self.assertEqual("Alice", query_user_json_response['username'])
        self.assertEqual("I love playing the piano and travelling.", query_user_json_response['about'])
        self.assertEqual(register_json_response['id'], query_user_json_response['id'])
        self.assertTrue(validate_uuid4_string(query_user_json_response['id']))

    def test_can_fetch_all_users(self):
        self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        })
        self.client.post('/users', json={
            "username": "Maria",
            "password": "27398273",
            "about": "I love playing the chess and dancing."
        })

        query_user_response = self.client.get('/users')
        query_user_json_response = query_user_response.get_json()

        self.assertEqual(200, query_user_response.status_code)
        self.assertEqual(2, len(query_user_json_response))

    def test_users_can_follow_other_users(self):
        register_first_user_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        }).get_json()
        register_second_user_response = self.client.post('/users', json={
            "username": "Maria",
            "password": "27398273",
            "about": "I love playing the chess and dancing."
        }).get_json()

        follow_response = self.client.post("/followings", json={"followerId": register_first_user_response['id'],
                                                                "followeeId": register_second_user_response['id']})

        self.assertEqual(201, follow_response.status_code)

    def test_can_fetch_followers(self):
        register_first_user_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        }).get_json()
        register_second_user_response = self.client.post('/users', json={
            "username": "Maria",
            "password": "27398273",
            "about": "I love playing the chess and dancing."
        }).get_json()

        follow_response = self.client.post("/followings", json={"followerId": register_first_user_response['id'],
                                                                "followeeId": register_second_user_response['id']})

        followees_response = self.client.get("/followings/%s/followees" % register_first_user_response['id'])

        followees_json_response = followees_response.get_json()
        self.assertEqual(201, follow_response.status_code)
        self.assertEqual(200, followees_response.status_code)

        self.assertEqual(1, len(followees_json_response))
        self.assertEqual(followees_json_response[0]['id'], register_second_user_response['id'])

    def test_can_fetch_the_wall(self):
        register_first_user_response = self.client.post('/users', json={
            "username": "Alice",
            "password": "alki324d",
            "about": "I love playing the piano and travelling."
        }).get_json()
        register_second_user_response = self.client.post('/users', json={
            "username": "Maria",
            "password": "27398273",
            "about": "I love playing the chess and dancing."
        }).get_json()

        follow_response = self.client.post("/followings", json={"followerId": register_first_user_response['id'],
                                                                "followeeId": register_second_user_response['id']})
        followees_response = self.client.get("/followings/%s/followees" % register_first_user_response['id'])

        followees_json_response = followees_response.get_json()

        self.client.post('/users/%s/timeline' % register_second_user_response['id'],
                         json={"text": "Hello everyone. I'm Maria."})

        wall_response = self.client.get("/users/%s/wall" % register_first_user_response['id'])

        wall_json_response = wall_response.get_json()

        self.assertEqual(201, follow_response.status_code)
        self.assertEqual(200, followees_response.status_code)
        self.assertEqual(200, wall_response.status_code)

        self.assertEqual(1, len(followees_json_response))
        self.assertEqual(followees_json_response[0]['id'], register_second_user_response['id'])
        self.assertEqual(1, len(wall_json_response))
