from unittest import TestCase

from apps.RESTAPI.__main__ import create_openchat_app


class TestRegistrationRequests(TestCase):
    def setUp(self):
        self.app = create_openchat_app(environment='development')
        self.client = self.app.test_client()

    def test_should_return_bar_request_on_invalid_body_format(self):
        error_response = self.client.post('/users', json=[])
        self.assertEqual(400, error_response.status_code)

    def test_should_return_not_found_on_inexistent_resource(self):
        error_response = self.client.post('/i_dont_exist', json=[])
        self.assertEqual(404, error_response.status_code)
