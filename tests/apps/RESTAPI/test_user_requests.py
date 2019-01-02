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
        self.client.post('/users', json=json.loads("""{
            "username" : "Maria",
            "password" : "27398273",
            "about" : "I love playing the chess and dancing."
        }"""))

        query_user_response = self.client.get('/users')
        query_user_json_response = json.loads(query_user_response.get_data(as_text=True))

        assert 200 == query_user_response.status_code
        assert len(query_user_json_response) == 2

    def test_users_can_follow_other_users(self):
        register_first_user_response = json.loads(self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }""")).get_data(as_text=True))
        register_second_user_response = json.loads(self.client.post('/users', json=json.loads("""{
            "username" : "Maria",
            "password" : "27398273",
            "about" : "I love playing the chess and dancing."
        }""")).get_data(as_text=True))

        follow_response = self.client.post("/followings", json=json.loads('{"followerId" : "%s","followeeId" : "%s"}' %
                                                                          (register_first_user_response['id'],
                                                                           register_second_user_response['id'])))

        assert 201 == follow_response.status_code

    def test_can_fetch_followers(self):
        register_first_user_response = json.loads(self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }""")).get_data(as_text=True))
        register_second_user_response = json.loads(self.client.post('/users', json=json.loads("""{
            "username" : "Maria",
            "password" : "27398273",
            "about" : "I love playing the chess and dancing."
        }""")).get_data(as_text=True))

        follow_response = self.client.post("/followings", json=json.loads('{"followerId" : "%s","followeeId" : "%s"}' %
                                                                          (register_first_user_response['id'],
                                                                           register_second_user_response['id'])))

        followees_response = self.client.get("/followings/%s/followees" % register_first_user_response['id'])

        followees_json_response = json.loads(followees_response.get_data(as_text=True))
        assert 201 == follow_response.status_code
        assert 200 == followees_response.status_code

        assert len(followees_json_response) == 1
        assert followees_json_response[0]['id'] == register_second_user_response['id']

    def test_can_fetch_the_wall(self):
        register_first_user_response = json.loads(self.client.post('/users', json=json.loads("""{
        "username" : "Alice",
        "password" : "alki324d",
        "about" : "I love playing the piano and travelling."
    }""")).get_data(as_text=True))
        register_second_user_response = json.loads(self.client.post('/users', json=json.loads("""{
            "username" : "Maria",
            "password" : "27398273",
            "about" : "I love playing the chess and dancing."
        }""")).get_data(as_text=True))

        self.client.post('/users/%s/timeline' % register_second_user_response['id'],
                         json=json.loads("""{"text" : "Hello everyone. I'm Maria."}"""))
        follow_response = self.client.post("/followings", json=json.loads('{"followerId" : "%s","followeeId" : "%s"}' %
                                                                          (register_first_user_response['id'],
                                                                           register_second_user_response['id'])))

        followees_response = self.client.get("/followings/%s/followees" % register_first_user_response['id'])

        followees_json_response = json.loads(followees_response.get_data(as_text=True))

        wall_response = self.client.get("/users/%s/wall" % register_first_user_response['id'])

        wall_json_response = json.loads(wall_response.get_data(as_text=True))

        assert 201 == follow_response.status_code
        assert 200 == followees_response.status_code
        assert 200 == wall_response.status_code

        assert len(followees_json_response) == 1
        assert followees_json_response[0]['id'] == register_second_user_response['id']
        assert len(wall_json_response) == 1
