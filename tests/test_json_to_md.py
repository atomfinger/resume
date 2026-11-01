from datetime import datetime
from typing import List
from unittest import TestCase

from parameterized import parameterized

from resume.json_to_md import get_header_information, convert_volunteer, convert_education, \
    convert_skill, \
    convert_award, convert_publication, convert_languages, convert_interests, format_date, convert_certificate, format_release_date, convert_talk, get_talks, get_other_projects, \
    get_markdown_content
from resume.resume_types import Basics, Location, Profile, Volunteer, Education, Skill, Award, Publication, Language, \
    Interest, Certificate, Resume, Project


class Test(TestCase):
    def test_get_header_information_verify_name(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[0], 'Tom Waits')

    def test_get_header_information_verify_title_line(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[1], '===================')

    def test_get_header_information_verify_newline_string(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[2], '  ')

    def test_get_header_information_verify_label(self):
        result = get_header_information(create_basics())
        self.assertEqual(result[3], '#### Singer/songwriter/musician/composer/actor')

    def test_parse_date_missing_date_and_default_error_should_be_thrown(self):
        with self.assertRaises(Exception) as context:
            format_date(None, None)
        self.assertTrue('Missing date' in str(context.exception))

    def test_convert_certificate_includes_issuer_and_date(self):
        certificate = Certificate(name='Certified Kubernetes Administrator', issuer='CNCF',
                                  date=datetime(1989, 6, 12))
        self.assertEqual(convert_certificate(certificate),
                         ' - **Certified Kubernetes Administrator**, CNCF (06.1989)')

    def test_convert_certificate_without_issuer_and_date_is_just_the_name(self):
        self.assertEqual(convert_certificate(Certificate(name='Foundational C#')), ' - **Foundational C#**')

    def test_release_date_only_shows_the_precision_it_has(self):
        self.assertEqual(format_release_date('2026-09-03'), '03.09.2026')
        self.assertEqual(format_release_date('2026-09'), '09.2026')
        self.assertEqual(format_release_date('2026'), '2026')

    def test_publication_with_only_month_and_year(self):
        publication = Publication('A talk', 'A conference', '2026-09', 'A summary', 'https://example.com/talk')
        self.assertEqual(convert_publication(publication),
                         '**[A talk (09.2026)](https://example.com/talk)** - A conference  A summary')

    def test_parse_date_missing_date_and_provided_default_should_be_returned(self):
        self.assertEqual(format_date(None, 'Current'), 'Current')

    def test_parse_date_actual_date_provided_should_be_returned_in_proper_string_form(self):
        self.assertEqual(format_date('1988-06-21', 'Current'), '06.1988')

    def test_convert_volunteer_verify_title_line(self):
        self.assertEqual(convert_volunteer(create_volunteer())[0],
                         '**Iron man**, '
                         '[The avengers](https://en.wikipedia.org/wiki/The_Avengers_(2012_film)) (06.1988 - Current)')

    @parameterized.expand([[1], [3]])
    def test_convert_volunteer_verify_empty_lines(self, index: int):
        result = convert_volunteer(create_volunteer())
        self.assertEqual(result[index], '  ')

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
        skill = Skill(['HTML', 'CSS', 'BRAINFUCK', 'Rockstar'], "Master", 'Programming languages')
        self.assertEqual(convert_skill(skill), f' - **Programming languages:** HTML, CSS, BRAINFUCK, Rockstar')

    def test_convert_award(self):
        award = Award('My mom', '1982-08-02', 'Got the coolest boy award', 'Coolest boy')
        self.assertEqual(convert_award(award), '**Coolest boy (My mom - 02.08.1982):** Got the coolest boy award')

    def test_convert_publication(self):
        publication = Publication('1984', 'Secker & Warburg', '1949-06-08',
                                  'The story takes place in an imagined future, the year 1984, when much of the world '
                                  'has fallen victim to perpetual war, omnipresent government surveillance, historical '
                                  'negationism, and propaganda.',
                                  'https://en.wikipedia.org/wiki/Nineteen_Eighty-Four'
                                  )
        result = convert_publication(publication)
        self.assertEqual(result, '**[1984 (08.06.1949)](https://en.wikipedia.org/wiki/Nineteen_Eighty-Four)** - '
                                 'Secker & Warburg  The story takes place in an imagined future, the year 1984, '
                                 'when much of the world has fallen victim to perpetual war, omnipresent government '
                                 'surveillance, historical negationism, and propaganda.')

    def test_convert_publication_when_no_publisher(self):
        publication = Publication('1984', None, '1949-06-08',
                                  'The story takes place in an imagined future, the year 1984, when much of the world '
                                  'has fallen victim to perpetual war, omnipresent government surveillance, historical '
                                  'negationism, and propaganda.',
                                  'https://en.wikipedia.org/wiki/Nineteen_Eighty-Four'
                                  )
        result = convert_publication(publication)
        self.assertEqual(result, '**[1984 (08.06.1949)](https://en.wikipedia.org/wiki/Nineteen_Eighty-Four)**  The '
                                 'story takes place in an imagined future, the year 1984, '
                                 'when much of the world has fallen victim to perpetual war, omnipresent government '
                                 'surveillance, historical negationism, and propaganda.')

    def test_convert_languages(self):
        languages = [Language('Master', 'English'), Language(None, 'Elvish'), Language('Beginner', 'Klingon')]
        result = convert_languages(languages)
        self.assertEqual(result[2], 'English, Elvish, Klingon')

    def test_convert_interests(self):
        interests = [Interest(['Dabbing', 'Pawning noobs', 'Loving my mum'], 'Being dope')]
        result = convert_interests(interests)
        self.assertEqual(result[2], ' - Being dope: Dabbing, Pawning noobs, Loving my mum')


def create_education() -> Education:
    return Education(
        institution='Awesome university',
        url='awesomeuniversity.com',
        area='Cool Course',
        study_type='Bachelors',
        start_date='1420-03-21',
        end_date='1337-4-21',
        score='N/A',
        courses=[
            'Being chill: The fundamentals',
            'Swag 101',
            'Dabbing'
        ]
    )


def create_volunteer() -> Volunteer:
    return Volunteer(
        organization='The avengers',
        position='Iron man',
        url='https://en.wikipedia.org/wiki/The_Avengers_(2012_film)',
        start_date='1988-06-21',
        end_date=None,
        summary='Worked with a group that battles horrors that might threaten earth',
        highlights=[
            'Fought Ultron',
            'Been in close combat with the Hulk',
            'Met literal norse gods',
            'Married',
            'Been pretty cool to Spiderman'
        ]
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


class TestMarkdownContent(TestCase):
    def test_summary_is_kept_as_one_line_of_text(self):
        resume = Resume(basics=Basics(name='Tom Waits', label='Musician', summary='A summary of a career', profiles=[]))
        lines = [line for category in get_markdown_content(resume) for line in category]
        self.assertIn('A summary of a career', lines)


class TestTalks(TestCase):
    def test_talks_are_the_projects_of_type_talk(self):
        talk = Project(name='A talk', type='talk')
        project = Project(name='A library')
        self.assertEqual(get_talks([talk, project]), [talk])
        self.assertEqual(get_other_projects([talk, project]), [project])

    def test_no_projects_means_no_talks(self):
        self.assertEqual(get_talks(None), [])
        self.assertEqual(get_other_projects(None), [])

    def test_convert_talk(self):
        talk = Project(name='Gleam and BEAM', type='talk', entity='JavaZone', start_date='2026-09',
                       description='A talk about Gleam.', url='https://example.com/video')
        self.assertEqual(convert_talk(talk),
                         '**[Gleam and BEAM (09.2026)](https://example.com/video)** - JavaZone  A talk about Gleam.')

    def test_markdown_lists_talks_apart_from_projects(self):
        resume = Resume(projects=[
            Project(name='A library', url='https://example.com/lib', description='A library.'),
            Project(name='A talk', type='talk', entity='A conference', start_date='2026-02',
                    url='https://example.com/talk', description='About things.')])
        lines = [line for category in get_markdown_content(resume) for line in category]
        self.assertIn('Public speaking', lines)
        self.assertIn('Projects', lines)
        speaking = lines.index('Public speaking')
        projects = lines.index('Projects')
        self.assertTrue(any('A talk' in line for line in lines[speaking:projects]) or
                        any('A talk' in line for line in lines[speaking:]))
        self.assertFalse(any('A library' in line for line in lines[speaking:projects]))
