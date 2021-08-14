import json
import os
from typing import List

from src.resume_types import Basics, Resume, resume_from_dict

NEW_LINE = ''


def get_contact_and_social_line(basics: Basics) -> List[str]:
    contact_and_links = [basics.email, basics.phone, f'[{basics.url}]({basics.url}']
    [contact_and_links.append(f'[{profile.username}@{profile.network}]({profile.url})') for profile in basics.profiles]
    return [f'###### {" - ".join([i for i in contact_and_links if i])}']


def get_header_information(basics: Basics) -> List[str]:
    return [
        basics.name,
        '===================',
        NEW_LINE,
        f'#### {basics.label}'
    ]


def convert_resume(resume: Resume) -> str:
    content = [
        get_header_information(resume.basics),
        get_contact_and_social_line(resume.basics)
    ]
    return os.linesep.join([item_line for category in content for item_line in category])


def do_conversion(source: str, dest: str):
    with open(source, 'r') as f:
        resume = resume_from_dict(json.loads(f.read()))
    markdown = convert_resume(resume)
    with open(dest, 'w') as f:
        f.write(markdown)
