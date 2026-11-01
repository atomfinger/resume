from unittest import TestCase

from resume.txt_to_morse_code import encrypt


class Test(TestCase):
    def test_letters_are_encoded(self):
        self.assertEqual(encrypt('SOS'), '... --- ... ')

    def test_underscore_is_encoded(self):
        self.assertEqual(encrypt('a_b'), '.- ..--.- -... ')

    def test_characters_without_morse_code_are_skipped_instead_of_failing(self):
        self.assertEqual(encrypt('E@E'), '. . ')
