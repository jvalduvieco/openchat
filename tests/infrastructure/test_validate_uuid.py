from unittest import TestCase
from uuid import uuid4

from infrastructure.uuid.validate_uuid import validate_uuid4_string


class TestValidateUUID4(TestCase):
    def test_can_validate_a_valid_uuid4(self):
        self.assertTrue(validate_uuid4_string(uuid4().__str__()))

    def test_can_validate_a_valid_uuid4_formatted_as_hex(self):
        self.assertTrue(validate_uuid4_string('89eb35868a8247a4A911758a62601cf7'))

    def test_fails_to_validate_an_invalid_uuid4(self):
        self.assertFalse(validate_uuid4_string('IamNotAUUID4'))

    def test_fails_to_validate_a_valid_hex_but_invalid_uuid4(self):
        self.assertFalse(validate_uuid4_string('89eb35868a8247a4c911758a62601cf7'))
