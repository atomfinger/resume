from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any, List, TypeVar, Callable, Type, cast

import dateutil.parser

T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


@dataclass
class Award:
    title: Optional[str] = None
    date: Optional[datetime] = None
    awarder: Optional[str] = None
    summary: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Award':
        assert isinstance(obj, dict)
        title = from_union([from_str, from_none], obj.get("title"))
        date = from_union([from_datetime, from_none], obj.get("date"))
        awarder = from_union([from_str, from_none], obj.get("awarder"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        return Award(title, date, awarder, summary)

    def to_dict(self) -> dict:
        result: dict = {"title": from_union([from_str, from_none], self.title),
                        "date": from_union([lambda x: x.isoformat(), from_none], self.date),
                        "awarder": from_union([from_str, from_none], self.awarder),
                        "summary": from_union([from_str, from_none], self.summary)}
        return result


@dataclass
class Location:
    address: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    region: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        address = from_union([from_str, from_none], obj.get("address"))
        postal_code = from_union([from_str, from_none], obj.get("postalCode"))
        city = from_union([from_str, from_none], obj.get("city"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        region = from_union([from_str, from_none], obj.get("region"))
        return Location(address, postal_code, city, country_code, region)

    def to_dict(self) -> dict:
        result: dict = {"address": from_union([from_str, from_none], self.address),
                        "postalCode": from_union([from_str, from_none], self.postal_code),
                        "city": from_union([from_str, from_none], self.city),
                        "countryCode": from_union([from_str, from_none], self.country_code),
                        "region": from_union([from_str, from_none], self.region)}
        return result


@dataclass
class Profile:
    network: Optional[str] = None
    username: Optional[str] = None
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Profile':
        assert isinstance(obj, dict)
        network = from_union([from_str, from_none], obj.get("network"))
        username = from_union([from_str, from_none], obj.get("username"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Profile(network, username, url)

    def to_dict(self) -> dict:
        result: dict = {"network": from_union([from_str, from_none], self.network),
                        "username": from_union([from_str, from_none], self.username),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Basics:
    name: Optional[str] = None
    label: Optional[str] = None
    image: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[Location] = None
    profiles: Optional[List[Profile]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Basics':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        label = from_union([from_str, from_none], obj.get("label"))
        image = from_union([from_str, from_none], obj.get("image"))
        email = from_union([from_str, from_none], obj.get("email"))
        phone = from_union([from_str, from_none], obj.get("phone"))
        url = from_union([from_str, from_none], obj.get("url"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        profiles = from_union([lambda x: from_list(Profile.from_dict, x), from_none], obj.get("profiles"))
        return Basics(name, label, image, email, phone, url, summary, location, profiles)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "label": from_union([from_str, from_none], self.label),
                        "image": from_union([from_str, from_none], self.image),
                        "email": from_union([from_str, from_none], self.email),
                        "phone": from_union([from_str, from_none], self.phone),
                        "url": from_union([from_str, from_none], self.url),
                        "summary": from_union([from_str, from_none], self.summary),
                        "location": from_union([lambda x: to_class(Location, x), from_none], self.location),
                        "profiles": from_union([lambda x: from_list(lambda x: to_class(Profile, x), x), from_none],
                                               self.profiles)}
        return result


@dataclass
class Education:
    institution: Optional[str] = None
    url: Optional[str] = None
    area: Optional[str] = None
    study_type: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    score: Optional[str] = None
    courses: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Education':
        assert isinstance(obj, dict)
        institution = from_union([from_str, from_none], obj.get("institution"))
        url = from_union([from_str, from_none], obj.get("url"))
        area = from_union([from_str, from_none], obj.get("area"))
        study_type = from_union([from_str, from_none], obj.get("studyType"))
        start_date = from_union([from_datetime, from_none], obj.get("startDate"))
        end_date = from_union([from_datetime, from_none], obj.get("endDate"))
        score = from_union([from_str, from_none], obj.get("score"))
        courses = from_union([lambda x: from_list(from_str, x), from_none], obj.get("courses"))
        return Education(institution, url, area, study_type, start_date, end_date, score, courses)

    def to_dict(self) -> dict:
        result: dict = {"institution": from_union([from_str, from_none], self.institution),
                        "url": from_union([from_str, from_none], self.url),
                        "area": from_union([from_str, from_none], self.area),
                        "studyType": from_union([from_str, from_none], self.study_type),
                        "startDate": from_union([lambda x: x.isoformat(), from_none], self.start_date),
                        "endDate": from_union([lambda x: x.isoformat(), from_none], self.end_date),
                        "score": from_union([from_str, from_none], self.score),
                        "courses": from_union([lambda x: from_list(from_str, x), from_none], self.courses)}
        return result


@dataclass
class Interest:
    name: Optional[str] = None
    keywords: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Interest':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        return Interest(name, keywords)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords)}
        return result


@dataclass
class Language:
    language: Optional[str] = None
    fluency: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Language':
        assert isinstance(obj, dict)
        language = from_union([from_str, from_none], obj.get("language"))
        fluency = from_union([from_str, from_none], obj.get("fluency"))
        return Language(language, fluency)

    def to_dict(self) -> dict:
        result: dict = {"language": from_union([from_str, from_none], self.language),
                        "fluency": from_union([from_str, from_none], self.fluency)}
        return result


@dataclass
class Project:
    name: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    url: Optional[str] = None
    roles: Optional[List[str]] = None
    entity: Optional[str] = None
    type: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        description = from_union([from_str, from_none], obj.get("description"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        start_date = from_union([from_datetime, from_none], obj.get("startDate"))
        end_date = from_union([from_datetime, from_none], obj.get("endDate"))
        url = from_union([from_str, from_none], obj.get("url"))
        roles = from_union([lambda x: from_list(from_str, x), from_none], obj.get("roles"))
        entity = from_union([from_str, from_none], obj.get("entity"))
        type = from_union([from_str, from_none], obj.get("type"))
        return Project(name, description, highlights, keywords, start_date, end_date, url, roles, entity, type)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "description": from_union([from_str, from_none], self.description),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords),
                        "startDate": from_union([lambda x: x.isoformat(), from_none], self.start_date),
                        "endDate": from_union([lambda x: x.isoformat(), from_none], self.end_date),
                        "url": from_union([from_str, from_none], self.url),
                        "roles": from_union([lambda x: from_list(from_str, x), from_none], self.roles),
                        "entity": from_union([from_str, from_none], self.entity),
                        "type": from_union([from_str, from_none], self.type)}
        return result


@dataclass
class Publication:
    name: Optional[str] = None
    publisher: Optional[str] = None
    release_date: Optional[datetime] = None
    website: Optional[str] = None
    summary: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Publication':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        publisher = from_union([from_str, from_none], obj.get("publisher"))
        release_date = from_union([from_datetime, from_none], obj.get("releaseDate"))
        website = from_union([from_str, from_none], obj.get("website"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        return Publication(name, publisher, release_date, website, summary)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "publisher": from_union([from_str, from_none], self.publisher),
                        "releaseDate": from_union([lambda x: x.isoformat(), from_none], self.release_date),
                        "website": from_union([from_str, from_none], self.website),
                        "summary": from_union([from_str, from_none], self.summary)}
        return result


@dataclass
class Reference:
    name: Optional[str] = None
    reference: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Reference':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        reference = from_union([from_str, from_none], obj.get("reference"))
        return Reference(name, reference)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "reference": from_union([from_str, from_none], self.reference)}
        return result


@dataclass
class Skill:
    name: Optional[str] = None
    level: Optional[str] = None
    keywords: Optional[List[str]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Skill':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        level = from_union([from_str, from_none], obj.get("level"))
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        return Skill(name, level, keywords)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "level": from_union([from_str, from_none], self.level),
                        "keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords)}
        return result


@dataclass
class Volunteer:
    organization: Optional[str] = None
    position: Optional[str] = None
    website: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    summary: Optional[str] = None
    highlights: Optional[List[str]] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Volunteer':
        assert isinstance(obj, dict)
        organization = from_union([from_str, from_none], obj.get("organization"))
        position = from_union([from_str, from_none], obj.get("position"))
        website = from_union([from_str, from_none], obj.get("website"))
        start_date = from_union([from_datetime, from_none], obj.get("startDate"))
        end_date = from_union([from_datetime, from_none], obj.get("endDate"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Volunteer(organization, position, website, start_date, end_date, summary, highlights, name)

    def to_dict(self) -> dict:
        result: dict = {"organization": from_union([from_str, from_none], self.organization),
                        "position": from_union([from_str, from_none], self.position),
                        "website": from_union([from_str, from_none], self.website),
                        "startDate": from_union([lambda x: x.isoformat(), from_none], self.start_date),
                        "endDate": from_union([lambda x: x.isoformat(), from_none], self.end_date),
                        "summary": from_union([from_str, from_none], self.summary),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "name": from_union([from_str, from_none], self.name)}
        return result


@dataclass
class Work:
    company: Optional[str] = None
    position: Optional[str] = None
    website: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    summary: Optional[str] = None
    highlights: Optional[List[str]] = None
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Work':
        assert isinstance(obj, dict)
        company = from_union([from_str, from_none], obj.get("company"))
        position = from_union([from_str, from_none], obj.get("position"))
        website = from_union([from_str, from_none], obj.get("website"))
        start_date = from_union([from_datetime, from_none], obj.get("startDate"))
        end_date = from_union([from_datetime, from_none], obj.get("endDate"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Work(company, position, website, start_date, end_date, summary, highlights, name)

    def to_dict(self) -> dict:
        result: dict = {"company": from_union([from_str, from_none], self.company),
                        "position": from_union([from_str, from_none], self.position),
                        "website": from_union([from_str, from_none], self.website),
                        "startDate": from_union([lambda x: x.isoformat(), from_none], self.start_date),
                        "endDate": from_union([lambda x: x.isoformat(), from_none], self.end_date),
                        "summary": from_union([from_str, from_none], self.summary),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "name": from_union([from_str, from_none], self.name)}
        return result


@dataclass
class Resume:
    basics: Optional[Basics] = None
    work: Optional[List[Work]] = None
    volunteer: Optional[List[Volunteer]] = None
    education: Optional[List[Education]] = None
    awards: Optional[List[Award]] = None
    publications: Optional[List[Publication]] = None
    skills: Optional[List[Skill]] = None
    languages: Optional[List[Language]] = None
    interests: Optional[List[Interest]] = None
    references: Optional[List[Reference]] = None
    projects: Optional[List[Project]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Resume':
        assert isinstance(obj, dict)
        basics = from_union([Basics.from_dict, from_none], obj.get("basics"))
        work = from_union([lambda x: from_list(Work.from_dict, x), from_none], obj.get("work"))
        volunteer = from_union([lambda x: from_list(Volunteer.from_dict, x), from_none], obj.get("volunteer"))
        education = from_union([lambda x: from_list(Education.from_dict, x), from_none], obj.get("education"))
        awards = from_union([lambda x: from_list(Award.from_dict, x), from_none], obj.get("awards"))
        publications = from_union([lambda x: from_list(Publication.from_dict, x), from_none], obj.get("publications"))
        skills = from_union([lambda x: from_list(Skill.from_dict, x), from_none], obj.get("skills"))
        languages = from_union([lambda x: from_list(Language.from_dict, x), from_none], obj.get("languages"))
        interests = from_union([lambda x: from_list(Interest.from_dict, x), from_none], obj.get("interests"))
        references = from_union([lambda x: from_list(Reference.from_dict, x), from_none], obj.get("references"))
        projects = from_union([lambda x: from_list(Project.from_dict, x), from_none], obj.get("projects"))
        return Resume(basics, work, volunteer, education, awards, publications, skills, languages, interests,
                      references, projects)

    def to_dict(self) -> dict:
        result: dict = {"basics": from_union([lambda x: to_class(Basics, x), from_none], self.basics),
                        "work": from_union([lambda x: from_list(lambda x: to_class(Volunteer, x), x), from_none],
                                           self.work),
                        "volunteer": from_union([lambda x: from_list(lambda x: to_class(Volunteer, x), x), from_none],
                                                self.volunteer),
                        "education": from_union([lambda x: from_list(lambda x: to_class(Education, x), x), from_none],
                                                self.education),
                        "awards": from_union([lambda x: from_list(lambda x: to_class(Award, x), x), from_none],
                                             self.awards), "publications": from_union(
                [lambda x: from_list(lambda x: to_class(Publication, x), x), from_none], self.publications),
                        "skills": from_union([lambda x: from_list(lambda x: to_class(Skill, x), x), from_none],
                                             self.skills),
                        "languages": from_union([lambda x: from_list(lambda x: to_class(Language, x), x), from_none],
                                                self.languages),
                        "interests": from_union([lambda x: from_list(lambda x: to_class(Interest, x), x), from_none],
                                                self.interests),
                        "references": from_union([lambda x: from_list(lambda x: to_class(Reference, x), x), from_none],
                                                 self.references),
                        "projects": from_union([lambda x: from_list(lambda x: to_class(Project, x), x), from_none],
                                               self.projects)}
        return result


def resume_from_dict(s: Any) -> Resume:
    return Resume.from_dict(s)


def resume_to_dict(x: Resume) -> Any:
    return to_class(Resume, x)
