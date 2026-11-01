import json
import os
import tempfile
from unittest import TestCase

from resume.simplify import simplify


class Test(TestCase):
    def test_the_short_version_keeps_talks_in_full_but_not_other_projects(self):
        resume = {'basics': {'name': 'A'}, 'interests': [{'name': 'x'}], 'education': [{'institution': 'a'}],
                  'projects': [{'name': 'A library'},
                               {'name': 'A talk', 'type': 'talk', 'entity': 'A conference', 'startDate': '2026-09',
                                'description': 'A long description', 'url': 'https://example.com',
                                'slides': 'https://example.com/slides'}]}
        with tempfile.TemporaryDirectory() as directory:
            origin = os.path.join(directory, 'in.json')
            destination = os.path.join(directory, 'out.json')
            with open(origin, 'w') as f:
                json.dump(resume, f)
            simplify(origin, destination)
            with open(destination) as f:
                result = json.load(f)
        self.assertEqual([project['name'] for project in result['projects']], ['A talk'])
        talk = result['projects'][0]
        self.assertEqual(talk['description'], 'A long description')
        self.assertEqual(talk['endDate'], talk['startDate'])
        self.assertNotIn('interests', result)
        self.assertNotIn('location', result['basics'])

    def test_no_talks_means_no_projects_at_all(self):
        resume = {'basics': {'name': 'A'}, 'education': [{'institution': 'a'}], 'projects': [{'name': 'A library'}]}
        with tempfile.TemporaryDirectory() as directory:
            origin = os.path.join(directory, 'in.json')
            destination = os.path.join(directory, 'out.json')
            with open(origin, 'w') as f:
                json.dump(resume, f)
            simplify(origin, destination)
            with open(destination) as f:
                result = json.load(f)
        self.assertNotIn('projects', result)
