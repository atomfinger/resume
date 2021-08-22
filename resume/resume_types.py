# This code parses date/times, so please
#
#     pip install python-dateutil
#
# To use this code, make sure you
#
#     import json
#
# and then, to convert JSON from a string, do
#
#     result = coordinate_from_dict(json.loads(json_string))

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


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


@dataclass
class Award:
    """e.g. Time Magazine"""
    awarder: Optional[str] = None
    date: Optional[str] = None
    """e.g. Received for my work with Quantum Physics"""
    summary: Optional[str] = None
    """e.g. One of the 100 greatest minds of the century"""
    title: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Award':
        assert isinstance(obj, dict)
        awarder = from_union([from_str, from_none], obj.get("awarder"))
        date = from_union([from_str, from_none], obj.get("date"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        title = from_union([from_str, from_none], obj.get("title"))
        return Award(awarder, date, summary, title)

    def to_dict(self) -> dict:
        result: dict = {}
        result["awarder"] = from_union([from_str, from_none], self.awarder)
        result["date"] = from_union([from_str, from_none], self.date)
        result["summary"] = from_union([from_str, from_none], self.summary)
        result["title"] = from_union([from_str, from_none], self.title)
        return result


@dataclass
class Location:
    """To add multiple address lines, use
    . For example, 1234 Glücklichkeit Straße
    Hinterhaus 5. Etage li.
    """
    address: Optional[str] = None
    city: Optional[str] = None
    """code as per ISO-3166-1 ALPHA-2, e.g. US, AU, IN"""
    country_code: Optional[str] = None
    postal_code: Optional[str] = None
    """The general region where you live. Can be a US state, or a province, for instance."""
    region: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        address = from_union([from_str, from_none], obj.get("address"))
        city = from_union([from_str, from_none], obj.get("city"))
        country_code = from_union([from_str, from_none], obj.get("countryCode"))
        postal_code = from_union([from_str, from_none], obj.get("postalCode"))
        region = from_union([from_str, from_none], obj.get("region"))
        return Location(address, city, country_code, postal_code, region)

    def to_dict(self) -> dict:
        result: dict = {"address": from_union([from_str, from_none], self.address),
                        "city": from_union([from_str, from_none], self.city),
                        "countryCode": from_union([from_str, from_none], self.country_code),
                        "postalCode": from_union([from_str, from_none], self.postal_code),
                        "region": from_union([from_str, from_none], self.region)}
        return result


@dataclass
class Profile:
    """e.g. Facebook or Twitter"""
    network: Optional[str] = None
    """e.g. http://twitter.example.com/neutralthoughts"""
    url: Optional[str] = None
    """e.g. neutralthoughts"""
    username: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Profile':
        assert isinstance(obj, dict)
        network = from_union([from_str, from_none], obj.get("network"))
        url = from_union([from_str, from_none], obj.get("url"))
        username = from_union([from_str, from_none], obj.get("username"))
        return Profile(network, url, username)

    def to_dict(self) -> dict:
        result: dict = {"network": from_union([from_str, from_none], self.network),
                        "url": from_union([from_str, from_none], self.url),
                        "username": from_union([from_str, from_none], self.username)}
        return result


@dataclass
class Basics:
    """e.g. thomas@gmail.com"""
    email: Optional[str] = None
    """URL (as per RFC 3986) to a image in JPEG or PNG format"""
    image: Optional[str] = None
    """e.g. Web Developer"""
    label: Optional[str] = None
    location: Optional[Location] = None
    name: Optional[str] = None
    """Phone numbers are stored as strings so use any format you like, e.g. 712-117-2923"""
    phone: Optional[str] = None
    """Specify any number of social networks that you participate in"""
    profiles: Optional[List[Profile]] = None
    """Write a short 2-3 sentence biography about yourself"""
    summary: Optional[str] = None
    """URL (as per RFC 3986) to your website, e.g. personal homepage"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Basics':
        assert isinstance(obj, dict)
        email = from_union([from_str, from_none], obj.get("email"))
        image = from_union([from_str, from_none], obj.get("image"))
        label = from_union([from_str, from_none], obj.get("label"))
        location = from_union([Location.from_dict, from_none], obj.get("location"))
        name = from_union([from_str, from_none], obj.get("name"))
        phone = from_union([from_str, from_none], obj.get("phone"))
        profiles = from_union([lambda x: from_list(Profile.from_dict, x), from_none], obj.get("profiles"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Basics(email, image, label, location, name, phone, profiles, summary, url)

    def to_dict(self) -> dict:
        result: dict = {"email": from_union([from_str, from_none], self.email),
                        "image": from_union([from_str, from_none], self.image),
                        "label": from_union([from_str, from_none], self.label),
                        "location": from_union([lambda x: to_class(Location, x), from_none], self.location),
                        "name": from_union([from_str, from_none], self.name),
                        "phone": from_union([from_str, from_none], self.phone),
                        "profiles": from_union([lambda x: from_list(lambda x: to_class(Profile, x), x), from_none],
                                               self.profiles),
                        "summary": from_union([from_str, from_none], self.summary),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Certificate:
    """e.g. 1989-06-12"""
    date: Optional[datetime] = None
    """e.g. CNCF"""
    issuer: Optional[str] = None
    """e.g. Certified Kubernetes Administrator"""
    name: Optional[str] = None
    """e.g. http://example.com"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Certificate':
        assert isinstance(obj, dict)
        date = from_union([from_datetime, from_none], obj.get("date"))
        issuer = from_union([from_str, from_none], obj.get("issuer"))
        name = from_union([from_str, from_none], obj.get("name"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Certificate(date, issuer, name, url)

    def to_dict(self) -> dict:
        result: dict = {"date": from_union([lambda x: x.isoformat(), from_none], self.date),
                        "issuer": from_union([from_str, from_none], self.issuer),
                        "name": from_union([from_str, from_none], self.name),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Education:
    """e.g. Arts"""
    area: Optional[str] = None
    """List notable courses/subjects"""
    courses: Optional[List[str]] = None
    end_date: Optional[str] = None
    """e.g. Massachusetts Institute of Technology"""
    institution: Optional[str] = None
    """grade point average, e.g. 3.67/4.0"""
    score: Optional[str] = None
    start_date: Optional[str] = None
    """e.g. Bachelor"""
    study_type: Optional[str] = None
    """e.g. http://facebook.example.com"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Education':
        assert isinstance(obj, dict)
        area = from_union([from_str, from_none], obj.get("area"))
        courses = from_union([lambda x: from_list(from_str, x), from_none], obj.get("courses"))
        end_date = from_union([from_str, from_none], obj.get("endDate"))
        institution = from_union([from_str, from_none], obj.get("institution"))
        score = from_union([from_str, from_none], obj.get("score"))
        start_date = from_union([from_str, from_none], obj.get("startDate"))
        study_type = from_union([from_str, from_none], obj.get("studyType"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Education(area, courses, end_date, institution, score, start_date, study_type, url)

    def to_dict(self) -> dict:
        result: dict = {"area": from_union([from_str, from_none], self.area),
                        "courses": from_union([lambda x: from_list(from_str, x), from_none], self.courses),
                        "endDate": from_union([from_str, from_none], self.end_date),
                        "institution": from_union([from_str, from_none], self.institution),
                        "score": from_union([from_str, from_none], self.score),
                        "startDate": from_union([from_str, from_none], self.start_date),
                        "studyType": from_union([from_str, from_none], self.study_type),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Interest:
    keywords: Optional[List[str]] = None
    """e.g. Philosophy"""
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Interest':
        assert isinstance(obj, dict)
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Interest(keywords, name)

    def to_dict(self) -> dict:
        result: dict = {"keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords),
                        "name": from_union([from_str, from_none], self.name)}
        return result


@dataclass
class Language:
    """e.g. Fluent, Beginner"""
    fluency: Optional[str] = None
    """e.g. English, Spanish"""
    language: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Language':
        assert isinstance(obj, dict)
        fluency = from_union([from_str, from_none], obj.get("fluency"))
        language = from_union([from_str, from_none], obj.get("language"))
        return Language(fluency, language)

    def to_dict(self) -> dict:
        result: dict = {"fluency": from_union([from_str, from_none], self.fluency),
                        "language": from_union([from_str, from_none], self.language)}
        return result


@dataclass
class Meta:
    """The schema version and any other tooling configuration lives here"""
    """URL (as per RFC 3986) to latest version of this document"""
    canonical: Optional[str] = None
    """Using ISO 8601 with YYYY-MM-DDThh:mm:ss"""
    last_modified: Optional[str] = None
    """A version field which follows semver - e.g. v1.0.0"""
    version: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        canonical = from_union([from_str, from_none], obj.get("canonical"))
        last_modified = from_union([from_str, from_none], obj.get("lastModified"))
        version = from_union([from_str, from_none], obj.get("version"))
        return Meta(canonical, last_modified, version)

    def to_dict(self) -> dict:
        result: dict = {"canonical": from_union([from_str, from_none], self.canonical),
                        "lastModified": from_union([from_str, from_none], self.last_modified),
                        "version": from_union([from_str, from_none], self.version)}
        return result


@dataclass
class Project:
    """Short summary of project. e.g. Collated works of 2017."""
    description: Optional[str] = None
    end_date: Optional[str] = None
    """Specify the relevant company/entity affiliations e.g. 'greenpeace', 'corporationXYZ'"""
    entity: Optional[str] = None
    """Specify multiple features"""
    highlights: Optional[List[str]] = None
    """Specify special elements involved"""
    keywords: Optional[List[str]] = None
    """e.g. The World Wide Web"""
    name: Optional[str] = None
    """Specify your role on this project or in company"""
    roles: Optional[List[str]] = None
    start_date: Optional[str] = None
    """e.g. 'volunteering', 'presentation', 'talk', 'application', 'conference'"""
    type: Optional[str] = None
    """e.g. http://www.computer.org/csdl/mags/co/1996/10/rx069-abs.html"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        end_date = from_union([from_str, from_none], obj.get("endDate"))
        entity = from_union([from_str, from_none], obj.get("entity"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        name = from_union([from_str, from_none], obj.get("name"))
        roles = from_union([lambda x: from_list(from_str, x), from_none], obj.get("roles"))
        start_date = from_union([from_str, from_none], obj.get("startDate"))
        type = from_union([from_str, from_none], obj.get("type"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Project(description, end_date, entity, highlights, keywords, name, roles, start_date, type, url)

    def to_dict(self) -> dict:
        result: dict = {"description": from_union([from_str, from_none], self.description),
                        "endDate": from_union([from_str, from_none], self.end_date),
                        "entity": from_union([from_str, from_none], self.entity),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords),
                        "name": from_union([from_str, from_none], self.name),
                        "roles": from_union([lambda x: from_list(from_str, x), from_none], self.roles),
                        "startDate": from_union([from_str, from_none], self.start_date),
                        "type": from_union([from_str, from_none], self.type),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Publication:
    """e.g. The World Wide Web"""
    name: Optional[str] = None
    """e.g. IEEE, Computer Magazine"""
    publisher: Optional[str] = None
    release_date: Optional[str] = None
    """Short summary of publication. e.g. Discussion of the World Wide Web, HTTP, HTML."""
    summary: Optional[str] = None
    """e.g. http://www.computer.org.example.com/csdl/mags/co/1996/10/rx069-abs.html"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Publication':
        assert isinstance(obj, dict)
        name = from_union([from_str, from_none], obj.get("name"))
        publisher = from_union([from_str, from_none], obj.get("publisher"))
        release_date = from_union([from_str, from_none], obj.get("releaseDate"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Publication(name, publisher, release_date, summary, url)

    def to_dict(self) -> dict:
        result: dict = {"name": from_union([from_str, from_none], self.name),
                        "publisher": from_union([from_str, from_none], self.publisher),
                        "releaseDate": from_union([from_str, from_none], self.release_date),
                        "summary": from_union([from_str, from_none], self.summary),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Reference:
    """e.g. Timothy Cook"""
    name: Optional[str] = None
    """e.g. Joe blogs was a great employee, who turned up to work at least once a week. He
    exceeded my expectations when it came to doing nothing.
    """
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
    """List some keywords pertaining to this skill"""
    keywords: Optional[List[str]] = None
    """e.g. Master"""
    level: Optional[str] = None
    """e.g. Web Development"""
    name: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Skill':
        assert isinstance(obj, dict)
        keywords = from_union([lambda x: from_list(from_str, x), from_none], obj.get("keywords"))
        level = from_union([from_str, from_none], obj.get("level"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Skill(keywords, level, name)

    def to_dict(self) -> dict:
        result: dict = {"keywords": from_union([lambda x: from_list(from_str, x), from_none], self.keywords),
                        "level": from_union([from_str, from_none], self.level),
                        "name": from_union([from_str, from_none], self.name)}
        return result


@dataclass
class Volunteer:
    end_date: Optional[str] = None
    """Specify accomplishments and achievements"""
    highlights: Optional[List[str]] = None
    """e.g. Facebook"""
    organization: Optional[str] = None
    """e.g. Software Engineer"""
    position: Optional[str] = None
    start_date: Optional[str] = None
    """Give an overview of your responsibilities at the company"""
    summary: Optional[str] = None
    """e.g. http://facebook.example.com"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Volunteer':
        assert isinstance(obj, dict)
        end_date = from_union([from_str, from_none], obj.get("endDate"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        organization = from_union([from_str, from_none], obj.get("organization"))
        position = from_union([from_str, from_none], obj.get("position"))
        start_date = from_union([from_str, from_none], obj.get("startDate"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Volunteer(end_date, highlights, organization, position, start_date, summary, url)

    def to_dict(self) -> dict:
        result: dict = {"endDate": from_union([from_str, from_none], self.end_date),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "organization": from_union([from_str, from_none], self.organization),
                        "position": from_union([from_str, from_none], self.position),
                        "startDate": from_union([from_str, from_none], self.start_date),
                        "summary": from_union([from_str, from_none], self.summary),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Work:
    """e.g. Social Media Company"""
    description: Optional[str] = None
    end_date: Optional[str] = None
    """Specify multiple accomplishments"""
    highlights: Optional[List[str]] = None
    """e.g. Menlo Park, CA"""
    location: Optional[str] = None
    """e.g. Facebook"""
    name: Optional[str] = None
    """e.g. Software Engineer"""
    position: Optional[str] = None
    start_date: Optional[str] = None
    """Give an overview of your responsibilities at the company"""
    summary: Optional[str] = None
    """e.g. http://facebook.example.com"""
    url: Optional[str] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Work':
        assert isinstance(obj, dict)
        description = from_union([from_str, from_none], obj.get("description"))
        end_date = from_union([from_str, from_none], obj.get("endDate"))
        highlights = from_union([lambda x: from_list(from_str, x), from_none], obj.get("highlights"))
        location = from_union([from_str, from_none], obj.get("location"))
        name = from_union([from_str, from_none], obj.get("name"))
        position = from_union([from_str, from_none], obj.get("position"))
        start_date = from_union([from_str, from_none], obj.get("startDate"))
        summary = from_union([from_str, from_none], obj.get("summary"))
        url = from_union([from_str, from_none], obj.get("url"))
        return Work(description, end_date, highlights, location, name, position, start_date, summary, url)

    def to_dict(self) -> dict:
        result: dict = {"description": from_union([from_str, from_none], self.description),
                        "endDate": from_union([from_str, from_none], self.end_date),
                        "highlights": from_union([lambda x: from_list(from_str, x), from_none], self.highlights),
                        "location": from_union([from_str, from_none], self.location),
                        "name": from_union([from_str, from_none], self.name),
                        "position": from_union([from_str, from_none], self.position),
                        "startDate": from_union([from_str, from_none], self.start_date),
                        "summary": from_union([from_str, from_none], self.summary),
                        "url": from_union([from_str, from_none], self.url)}
        return result


@dataclass
class Resume:
    """link to the version of the schema that can validate the resume"""
    schema: Optional[str] = None
    """Specify any awards you have received throughout your professional career"""
    awards: Optional[List[Award]] = None
    basics: Optional[Basics] = None
    """Specify any certificates you have received throughout your professional career"""
    certificates: Optional[List[Certificate]] = None
    education: Optional[List[Education]] = None
    interests: Optional[List[Interest]] = None
    """List any other languages you speak"""
    languages: Optional[List[Language]] = None
    """The schema version and any other tooling configuration lives here"""
    meta: Optional[Meta] = None
    """Specify career projects"""
    projects: Optional[List[Project]] = None
    """Specify your publications through your career"""
    publications: Optional[List[Publication]] = None
    """List references you have received"""
    references: Optional[List[Reference]] = None
    """List out your professional skill-set"""
    skills: Optional[List[Skill]] = None
    volunteer: Optional[List[Volunteer]] = None
    work: Optional[List[Work]] = None

    @staticmethod
    def from_dict(obj: Any) -> 'Resume':
        assert isinstance(obj, dict)
        schema = from_union([from_str, from_none], obj.get("$schema"))
        awards = from_union([lambda x: from_list(Award.from_dict, x), from_none], obj.get("awards"))
        basics = from_union([Basics.from_dict, from_none], obj.get("basics"))
        certificates = from_union([lambda x: from_list(Certificate.from_dict, x), from_none], obj.get("certificates"))
        education = from_union([lambda x: from_list(Education.from_dict, x), from_none], obj.get("education"))
        interests = from_union([lambda x: from_list(Interest.from_dict, x), from_none], obj.get("interests"))
        languages = from_union([lambda x: from_list(Language.from_dict, x), from_none], obj.get("languages"))
        meta = from_union([Meta.from_dict, from_none], obj.get("meta"))
        projects = from_union([lambda x: from_list(Project.from_dict, x), from_none], obj.get("projects"))
        publications = from_union([lambda x: from_list(Publication.from_dict, x), from_none], obj.get("publications"))
        references = from_union([lambda x: from_list(Reference.from_dict, x), from_none], obj.get("references"))
        skills = from_union([lambda x: from_list(Skill.from_dict, x), from_none], obj.get("skills"))
        volunteer = from_union([lambda x: from_list(Volunteer.from_dict, x), from_none], obj.get("volunteer"))
        work = from_union([lambda x: from_list(Work.from_dict, x), from_none], obj.get("work"))
        return Resume(schema, awards, basics, certificates, education, interests, languages, meta, projects,
                          publications, references, skills, volunteer, work)

    def to_dict(self) -> dict:
        result: dict = {"$schema": from_union([from_str, from_none], self.schema),
                        "awards": from_union([lambda x: from_list(lambda x: to_class(Award, x), x), from_none],
                                             self.awards),
                        "basics": from_union([lambda x: to_class(Basics, x), from_none], self.basics),
                        "certificates": from_union(
                            [lambda x: from_list(lambda x: to_class(Certificate, x), x), from_none],
                            self.certificates),
                        "education": from_union([lambda x: from_list(lambda x: to_class(Education, x), x), from_none],
                                                self.education),
                        "interests": from_union([lambda x: from_list(lambda x: to_class(Interest, x), x), from_none],
                                                self.interests),
                        "languages": from_union([lambda x: from_list(lambda x: to_class(Language, x), x), from_none],
                                                self.languages),
                        "meta": from_union([lambda x: to_class(Meta, x), from_none], self.meta),
                        "projects": from_union([lambda x: from_list(lambda x: to_class(Project, x), x), from_none],
                                               self.projects), "publications": from_union(
                [lambda x: from_list(lambda x: to_class(Publication, x), x), from_none],
                self.publications),
                        "references": from_union([lambda x: from_list(lambda x: to_class(Reference, x), x), from_none],
                                                 self.references),
                        "skills": from_union([lambda x: from_list(lambda x: to_class(Skill, x), x), from_none],
                                             self.skills),
                        "volunteer": from_union([lambda x: from_list(lambda x: to_class(Volunteer, x), x), from_none],
                                                self.volunteer),
                        "work": from_union([lambda x: from_list(lambda x: to_class(Work, x), x), from_none], self.work)}
        return result


def resume_from_dict(s: Any) -> Resume:
    return Resume.from_dict(s)


def resume_to_dict(x: Resume) -> Any:
    return to_class(Resume, x)
