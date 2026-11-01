from unittest import TestCase

from resume.json_to_pptx import contact_line
from resume.resume_types import Basics


class Test(TestCase):
    def test_contact_line_with_an_email_and_a_website(self):
        basics = Basics(name='Tom Waits', email='waits@tom.com', url='https://example.com')
        self.assertEqual(contact_line(basics), 'waits@tom.com or https://example.com')

    def test_contact_line_without_an_email_is_just_the_website(self):
        basics = Basics(name='Tom Waits', url='https://example.com')
        self.assertEqual(contact_line(basics), 'https://example.com')
