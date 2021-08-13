from typing import List
from unittest import TestCase

from json_to_md.json_to_md import get_header_information
from resume_parser.resume_types import Basics, Profile, Location


class Test(TestCase):
    def test_get_header_information_verify_name(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[0], 'Tom Waits')
        self.assertEqual(result[1], '===================')
        self.assertEqual(result[2], '')
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')

    def test_get_header_information_verify_title_line(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[1], '===================')
        self.assertEqual(result[2], '')
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')

    def test_get_header_information_verify_newline_string(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[2], '')
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')

    def test_get_header_information_verify_label(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')


def create_basics() -> Basics:
    return Basics(
        name='Tom Waits',
        label='Singer/songwriter/musician/composer/actor',
        image='',
        email='waits@tom.com',
        phone="1111 111 1111",
        url='tomwaits.com',
        summary='Thomas Alan Waits is an American singer, songwriter, musician, composer, and actor. His lyrics often '
                'focus on the underbelly of society and are delivered in his trademark deep, gravelly voice.',
        location=Location('', '', '', '', ''),
        profiles=create_profiles()

    )


def create_profiles() -> List[Profile]:
    return [
        Profile('Facebook', 'tomwaits', 'https://www.facebook.com/tomwaits')
    ]
