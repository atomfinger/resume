import json
import os
from datetime import datetime
from typing import List

from resume.resume_types import Basics, Resume, resume_from_dict, Volunteer, Education, Skill, Award

NEW_LINE = ''
DASH_LINE = '----------'


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
        get_contact_and_social_line(resume.basics),
        convert_volunteers("Experience", resume.work),
        convert_educations(resume.education),
        convert_volunteers("Volunteer", resume.volunteer),
        convert_skills(resume.skills)
    ]
    return os.linesep.join([item_line for category in content for item_line in category])


def parse_date(date: datetime, default: str = None) -> str:
    if not date and not default:
        raise TypeError("Missing date")
    if not date:
        return default
    return date.strftime('%m.%Y')


def convert_education(education: Education) -> List[str]:
    start_date = parse_date(education.start_date)
    end_date = parse_date(education.end_date, "Current")
    content = [
        f'**{education.study_type}, {education.area}**, {education.institution}({start_date} - {end_date})'
    ]
    for course in education.courses:
        content.append(f' * {course}')
    return content


def convert_educations(educations: List[Education]) -> List[str]:
    if len(educations) == 0:
        return []
    content = [
        "Education",
        DASH_LINE
    ]
    for education in educations:
        for line in convert_education(education):
            content.append(line)
        content.append(NEW_LINE)


def convert_volunteer(volunteer: Volunteer) -> List[str]:
    start_date = parse_date(volunteer.start_date)
    end_date = parse_date(volunteer.end_date, "Current")
    content = [
        f'**{volunteer.position}**, {volunteer.name}({start_date} - {end_date})',
        NEW_LINE,
        volunteer.summary,
        NEW_LINE
    ]
    [content.append(f' * {highlight}') for highlight in volunteer.highlights]
    return content


def convert_volunteers(title: str, volunteers: List[Volunteer]) -> List[str]:
    if len(volunteers) == 0:
        return []
    content = [
        title,
        DASH_LINE
    ]
    for volunteer in volunteers:
        for line in convert_volunteer(volunteer):
            content.append(line)
        content.append(NEW_LINE)
    return content


def convert_skill(skill: Skill) -> str:
    return f'**{skill.name}:** {", ".join(skill.keywords)}'


def convert_skills(skills: List[Skill]) -> List[str]:
    if len(skills) == 0:
        return []
    content = [
        "Skills",
        DASH_LINE
    ]
    [content.append(convert_skill(skill)) and content.append(NEW_LINE) for skill in skills]
    return content


def convert_award(award: Award) -> str:
    return f'**{award.title} ({award.awarder} - {award.date.strftime("%d.%m.%Y")}):** {award.summary}'


def convert_awards(awards: List[Award]) -> List[str]:
    if len(awards) == 0:
        return []
    content = [
        "Awards",
        DASH_LINE
    ]
    [content.append(convert_award(award)) and content.append(NEW_LINE) for award in awards]
    return content


def do_conversion(source: str, dest: str):
    with open(source, 'r') as f:
        resume = resume_from_dict(json.loads(f.read()))
    markdown = convert_resume(resume)
    with open(dest, 'w') as f:
        f.write(markdown)
