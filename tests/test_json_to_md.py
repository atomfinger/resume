import datetime
from typing import List
from unittest import TestCase

from parameterized import parameterized

from resume.json_to_md import get_header_information, parse_date, convert_volunteer, convert_education, convert_skill, \
    convert_award
from resume.resume_types import Basics, Location, Profile, Volunteer, Education, Skill, Award


class Test(TestCase):
    def test_get_header_information_verify_name(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[0], 'Tom Waits')

    def test_get_header_information_verify_title_line(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[1], '===================')

    def test_get_header_information_verify_newline_string(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[2], '')

    def test_get_header_information_verify_label(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')

    def test_parse_date_missing_date_and_default_error_should_be_thrown(self):
        with self.assertRaises(Exception) as context:
            parse_date(None, None)
        self.assertTrue('Missing date' in str(context.exception))

    def test_parse_date_missing_date_and_provided_default_should_be_returned(self):
        self.assertEqual(parse_date(None, 'Current'), 'Current')

    def test_parse_date_actual_date_provided_should_be_returned_in_proper_string_form(self):
        self.assertEqual(parse_date(datetime.datetime(1988, 6, 21), 'Current'), '06.1988')

    def test_convert_volunteer_verify_title_line(self):
        self.assertEqual(convert_volunteer(create_volunteer())[0],
                         '**Iron man**, '
                         '[The avengers](https://en.wikipedia.org/wiki/The_Avengers_(2012_film))(06.1988 - Current)')

    @parameterized.expand([[1], [3]])
    def test_convert_volunteer_verify_empty_lines(self, index: int):
        result = convert_volunteer(create_volunteer())
        self.assertEqual(result[index], '')

    def test_convert_volunteer_verify_summary_line(self):
        result = convert_volunteer(create_volunteer())
        self.assertEqual(result[2], 'Worked with a group that battles horrors that might threaten earth')

    @parameterized.expand([
        [4, ' * Fought Ultron'],
        [5, ' * Been in close combat with the Hulk'],
        [6, ' * Met literal norse gods'],
        [7, ' * Married'],
        [8, ' * Been pretty cool to Spiderman']
    ])
    def test_convert_volunteer_verify_highlights(self, index: int, expected_result: str):
        result = convert_volunteer(create_volunteer())
        self.assertEqual(result[index], expected_result)

    def test_convert_education_verify_title_line(self):
        result = convert_education(create_education())
        self.assertTrue(result[0], '**Bachelor, Cool Course**, Awesome University (03.420 - 04.1337)')

    @parameterized.expand([
        [1, ' * Being chill: The fundamentals'],
        [2, ' * Swag 101'],
        [3, ' * Dabbing']
    ])
    def test_convert_education_verify_courses(self, index: int, expected_result: str):
        result = convert_education(create_education())
        self.assertTrue(result[index], expected_result)

    def test_convert_skills(self):
        skill = Skill('Programming languages', "Master", ['HTML', 'CSS', 'BRAINFUCK', 'Rockstar'])
        self.assertEqual(convert_skill(skill), f'**Programming languages:** HTML, CSS, BRAINFUCK, Rockstar')

    def test_convert_award(self):
        award = Award('Coolest boy', datetime.datetime(1982, 8, 2), 'My mom', 'Got the coolest boy award')
        self.assertEqual(convert_award(award), '**Coolest boy (My mom - 02.08.1982):** Got the coolest boy award')


def create_education() -> Education:
    return Education(
        institution='Awesome university',
        url='awesomeuniversity.com',
        area='Cool Course',
        study_type='Bachelors',
        start_date=datetime.datetime(420, 3, 21),
        end_date=datetime.datetime(1337, 4, 21),
        score='N/A',
        courses= [
            'Being chill: The fundamentals',
            'Swag 101',
            'Dabbing'
        ]
    )


def create_volunteer() -> Volunteer:
    return Volunteer(
        name='The avengers',
        position='Iron man',
        url='https://en.wikipedia.org/wiki/The_Avengers_(2012_film)',
        start_date=datetime.datetime(1988, 6, 21),
        end_date=None,
        summary='Worked with a group that battles horrors that might threaten earth',
        highlights=[
            'Fought Ultron',
            'Been in close combat with the Hulk',
            'Met literal norse gods',
            'Married',
            'Been pretty cool to Spiderman'
        ],
        organization=None
    )


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
