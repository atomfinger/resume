import json
import os
import tempfile
from unittest import TestCase

from resume.json_to_yaml import convert_to_yaml
from resume.resume_types import resume_from_dict


class Test(TestCase):
    def test_every_section_in_the_resume_can_be_converted(self):
        # Guards against adding a section to resume.json that the converter can't represent.
        root = os.path.join(os.path.dirname(__file__), '..', 'resume.json')
        with open(root) as f:
            resume = resume_from_dict(json.load(f))
        with tempfile.TemporaryDirectory() as directory:
            destination = os.path.join(directory, 'resume.yml')
            convert_to_yaml(resume, destination)
            with open(destination) as f:
                content = f.read()
        self.assertIn('certificates', content)
        self.assertIn('Confluent Certified Developer for Apache Kafka', content)
