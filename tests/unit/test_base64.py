"""
Test base64
"""
import unittest

from nose_parameterized import parameterized

import base64

from scripts.better_base64 import BetterBase64


class Base64Test(unittest.TestCase):
    """
    Base64 tests
    """
    @parameterized.expand([
        "sdasdhas9d8has8djasijd0as9as9dddddddddddddddddddddddd68876hhhhhhhhhhhhhhhhhhhhhhhhhggggggggggggggggijgr"
        "j8f8fg8ufg89fg89hfgh9fgh9gf",
        "Lorem ipsum dolor sit amet enim. Etiam ullamcorper. Suspendisse a pellentesque dui, non felis. Maecenas malesuada elit lectus felis, malesuada ultricies."
    ])
    def test_base64_encode(self, str_to_encode):
        """
        Test base64 encode

        :param str str_to_encode: String to encode.
        """
        # Given
        encoded_str_by_external_lib = base64.b64encode(str_to_encode.encode('utf-8')).decode("utf-8")

        # When
        better_encoded_str = BetterBase64.encode(str_to_encode)

        # Then
        self.assertEquals(base64.b64decode(encoded_str_by_external_lib), base64.b64decode(better_encoded_str))

    def test_base64_encode_using_content_from_file(self):
        """
        Test base64 encode using content from file.
        """
        # Given
        with open('/project/base64.txt', 'r') as file:
            content = file.read()
        encoded_str_by_external_lib = base64.b64encode(content.encode('utf-8')).decode("utf-8")
        # When
        better_encoded_str = BetterBase64.encode(content)

        # Then
        self.assertEquals(base64.b64decode(encoded_str_by_external_lib), base64.b64decode(better_encoded_str))
