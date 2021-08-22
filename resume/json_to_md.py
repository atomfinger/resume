import os
from datetime import datetime
from typing import List, Optional, Union

import mdformat

from resume.resume_types import Basics, Volunteer, Education, Skill, Award, Publication, Language, Interest, \
    Project, Reference, Work, Resume

NEW_LINE = '  '
DASH_LINE = '----------'


def get_contact_and_social_line(basics: Basics) -> List[str]:
    contact_and_links = [basics.email, basics.phone, f'[{basics.url}]({basics.url})']
    [contact_and_links.append(f'[{profile.username}@{profile.network}]({profile.url})') for profile in basics.profiles]
    return [f'###### {" - ".join([i for i in contact_and_links if i])}']


def get_header_information(basics: Basics) -> List[str]:
    return [
        basics.name,
        '===================',
        NEW_LINE,
        f'#### {basics.label}'
    ]


def get_markdown_content(resume: Resume) -> list[Union[list[str], str]]:
    content: list[Union[list[str], str]] = []
    if resume.basics:
        content.append(get_header_information(resume.basics))
        content.append(get_contact_and_social_line(resume.basics))
        content.append(NEW_LINE)
        content.append(resume.basics.summary)
        content.append(NEW_LINE)
    if resume.work:
        content.append(convert_works("Experience", resume.work))
        content.append(NEW_LINE)
    if resume.education:
        content.append(convert_educations(resume.education))
        content.append(NEW_LINE)
    if resume.volunteer:
        content.append(convert_volunteers("Volunteer", resume.volunteer))
        content.append(NEW_LINE)
    if resume.skills:
        content.append(convert_skills(resume.skills))
        content.append(NEW_LINE)
    if resume.publications:
        content.append(convert_publications(resume.publications))
        content.append(NEW_LINE)
    if resume.languages:
        content.append(convert_languages(resume.languages))
        content.append(NEW_LINE)
    if resume.interests:
        content.append(convert_interests(resume.interests))
        content.append(NEW_LINE)
    if resume.projects:
        content.append(convert_projects(resume.projects))
        content.append(NEW_LINE)
    return content


def convert_to_markdown(resume: Resume, destination: str):
    content = get_markdown_content(resume)
    markdown = os.linesep.join([item_line for category in content for item_line in category])
    markdown = mdformat.text(markdown, options={
        'wrap': 120
    })
    with open(destination, 'w+') as f:
        f.write(markdown)


def date_to_string(date: datetime) -> str:
    return date.strftime('%m.%Y')


def string_to_date(date: str) -> datetime:
    return datetime.strptime(date, '%Y-%m-%d')


def format_date(date: Optional[str], default: str = None) -> str:
    if not date and not default:
        raise TypeError("Missing date")
    if not date:
        return default
    return date_to_string(string_to_date(date))


def convert_education(education: Education) -> List[str]:
    start_date = format_date(education.start_date)
    end_date = format_date(education.end_date, "Current")
    content = [
        f'**{education.study_type}, {education.area}**, '
        f'[{education.institution}]({education.url}) ({start_date} - {end_date}) '
    ]
    if education.courses:
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
    return content


def convert_volunteer(volunteer: Volunteer) -> List[str]:
    start_date = format_date(volunteer.start_date)
    end_date = format_date(volunteer.end_date, "Current")
    content = [
        f'**{volunteer.position}**, [{volunteer.organization}]({volunteer.url}) ({start_date} - {end_date})',
        NEW_LINE,
        volunteer.summary,
        NEW_LINE
    ]
    [content.append(f' * {highlight}') for highlight in volunteer.highlights]
    return content


def convert_volunteers(title: str, volunteers: List[Volunteer]) -> List[str]:
    if not volunteers or len(volunteers) == 0:
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


def convert_work(work: Work) -> List[str]:
    start_date = format_date(work.start_date)
    end_date = format_date(work.end_date, "Current")
    content = [
        f'**{work.position}**, [{work.name}]({work.url}) ({start_date} - {end_date})',
        NEW_LINE,
        work.summary,
        NEW_LINE
    ]
    [content.append(f' * {highlight}') for highlight in work.highlights]
    return content


def convert_works(title: str, works: List[Work]) -> List[str]:
    if not works or len(works) == 0:
        return []
    content = [
        title,
        DASH_LINE
    ]
    for volunteer in works:
        for line in convert_work(volunteer):
            content.append(line)
        content.append(NEW_LINE)
    return content


def convert_skill(skill: Skill) -> str:
    return f' - **{skill.name}:** {", ".join(skill.keywords)}'


def convert_skills(skills: List[Skill]) -> List[str]:
    if len(skills) == 0:
        return []
    content = [
        "Skills",
        DASH_LINE
    ]
    [content.append(convert_skill(skill)) for skill in skills]
    return content


def convert_award(award: Award) -> str:
    return f'**{award.title} ({award.awarder} - {string_to_date(award.date).strftime("%d.%m.%Y")}):** {award.summary}'


def convert_awards(awards: List[Award]) -> List[str]:
    if len(awards) == 0:
        return []
    content = [
        "Awards",
        DASH_LINE
    ]
    [content.append(convert_award(award)) and content.append(NEW_LINE) for award in awards]
    return content


def convert_publication(publication: Publication) -> str:
    publisher_text = ''
    if publication.publisher:
        publisher_text = f' - {publication.publisher}'
    return f'**[{publication.name} ' \
           f'({string_to_date(publication.release_date).strftime("%d.%m.%Y")})]({publication.url})**' \
           f'{publisher_text}  {publication.summary}'


def convert_publications(publications: List[Publication]) -> List[str]:
    if len(publications) == 0:
        return []
    content = [
        "Publications",
        DASH_LINE
    ]
    [content.append(convert_publication(publication)) and content.append(NEW_LINE) for publication in publications]
    return content


def convert_languages(languages: List[Language]) -> List[str]:
    if len(languages) == 0:
        return []
    content = [
        "Languages",
        DASH_LINE,
        ', '.join([language.language for language in languages])
    ]
    return content


def convert_interests(interests: List[Interest]) -> List[str]:
    if len(interests) == 0:
        return []
    content = [
        "Interests",
        DASH_LINE
    ]
    for interest in interests:
        content.append(f' - {interest.name}: {", ".join(interest.keywords)}')
    return content


def convert_project(project: Project) -> List[str]:
    start_date = format_date(project.start_date)
    end_date = format_date(project.end_date, "Current")
    roles = ''
    if project.roles:
        roles = f' - {", ".join(project.roles)}'
    content = [
        f'**[{project.name} ({start_date} - {end_date})]({project.url})**{roles}',
        NEW_LINE,
        project.description,
        NEW_LINE
    ]
    if project.highlights:
        [content.append(f' * {highlight}') for highlight in project.highlights]
    return content


def convert_projects(projects: List[Project]) -> List[str]:
    if not projects or len(projects) == 0:
        return []
    content = [
        "Projects",
        DASH_LINE
    ]
    for project in projects:
        for line in convert_project(project):
            content.append(line)
        content.append(NEW_LINE)
    return content


def convert_references(references: List[Reference]) -> List[str]:
    raise NotImplementedError('Not yet implemented')
