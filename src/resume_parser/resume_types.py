from datetime import datetime
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
import dateutil.parser


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    return dateutil.parser.parse(x)


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


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


class Award:
    title: str
    date: datetime
    awarder: str
    summary: str

    def __init__(self, title: str, date: datetime, awarder: str, summary: str) -> None:
        self.title = title
        self.date = date
        self.awarder = awarder
        self.summary = summary

    @staticmethod
    def from_dict(obj: Any) -> 'Award':
        assert isinstance(obj, dict)
        title = from_str(obj.get("title"))
        date = from_datetime(obj.get("date"))
        awarder = from_str(obj.get("awarder"))
        summary = from_str(obj.get("summary"))
        return Award(title, date, awarder, summary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["title"] = from_str(self.title)
        result["date"] = self.date.isoformat()
        result["awarder"] = from_str(self.awarder)
        result["summary"] = from_str(self.summary)
        return result


class Location:
    address: str
    postal_code: str
    city: str
    country_code: str
    region: str

    def __init__(self, address: str, postal_code: str, city: str, country_code: str, region: str) -> None:
        self.address = address
        self.postal_code = postal_code
        self.city = city
        self.country_code = country_code
        self.region = region

    @staticmethod
    def from_dict(obj: Any) -> 'Location':
        assert isinstance(obj, dict)
        address = from_str(obj.get("address"))
        postal_code = from_str(obj.get("postalCode"))
        city = from_str(obj.get("city"))
        country_code = from_str(obj.get("countryCode"))
        region = from_str(obj.get("region"))
        return Location(address, postal_code, city, country_code, region)

    def to_dict(self) -> dict:
        result: dict = {}
        result["address"] = from_str(self.address)
        result["postalCode"] = from_str(self.postal_code)
        result["city"] = from_str(self.city)
        result["countryCode"] = from_str(self.country_code)
        result["region"] = from_str(self.region)
        return result


class Profile:
    network: str
    username: str
    url: str

    def __init__(self, network: str, username: str, url: str) -> None:
        self.network = network
        self.username = username
        self.url = url

    @staticmethod
    def from_dict(obj: Any) -> 'Profile':
        assert isinstance(obj, dict)
        network = from_str(obj.get("network"))
        username = from_str(obj.get("username"))
        url = from_str(obj.get("url"))
        return Profile(network, username, url)

    def to_dict(self) -> dict:
        result: dict = {}
        result["network"] = from_str(self.network)
        result["username"] = from_str(self.username)
        result["url"] = from_str(self.url)
        return result


class Basics:
    name: str
    label: str
    image: str
    email: str
    phone: str
    url: str
    summary: str
    location: Location
    profiles: List[Profile]

    def __init__(self, name: str, label: str, image: str, email: str, phone: str, url: str, summary: str, location: Location, profiles: List[Profile]) -> None:
        self.name = name
        self.label = label
        self.image = image
        self.email = email
        self.phone = phone
        self.url = url
        self.summary = summary
        self.location = location
        self.profiles = profiles

    @staticmethod
    def from_dict(obj: Any) -> 'Basics':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        label = from_str(obj.get("label"))
        image = from_str(obj.get("image"))
        email = from_str(obj.get("email"))
        phone = from_str(obj.get("phone"))
        url = from_str(obj.get("url"))
        summary = from_str(obj.get("summary"))
        location = Location.from_dict(obj.get("location"))
        profiles = from_list(Profile.from_dict, obj.get("profiles"))
        return Basics(name, label, image, email, phone, url, summary, location, profiles)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["label"] = from_str(self.label)
        result["image"] = from_str(self.image)
        result["email"] = from_str(self.email)
        result["phone"] = from_str(self.phone)
        result["url"] = from_str(self.url)
        result["summary"] = from_str(self.summary)
        result["location"] = to_class(Location, self.location)
        result["profiles"] = from_list(lambda x: to_class(Profile, x), self.profiles)
        return result


class Education:
    institution: str
    url: str
    area: str
    study_type: str
    start_date: datetime
    end_date: datetime
    score: str
    courses: List[str]

    def __init__(self, institution: str, url: str, area: str, study_type: str, start_date: datetime, end_date: datetime, score: str, courses: List[str]) -> None:
        self.institution = institution
        self.url = url
        self.area = area
        self.study_type = study_type
        self.start_date = start_date
        self.end_date = end_date
        self.score = score
        self.courses = courses

    @staticmethod
    def from_dict(obj: Any) -> 'Education':
        assert isinstance(obj, dict)
        institution = from_str(obj.get("institution"))
        url = from_str(obj.get("url"))
        area = from_str(obj.get("area"))
        study_type = from_str(obj.get("studyType"))
        start_date = from_datetime(obj.get("startDate"))
        end_date = from_datetime(obj.get("endDate"))
        score = from_str(obj.get("score"))
        courses = from_list(from_str, obj.get("courses"))
        return Education(institution, url, area, study_type, start_date, end_date, score, courses)

    def to_dict(self) -> dict:
        result: dict = {}
        result["institution"] = from_str(self.institution)
        result["url"] = from_str(self.url)
        result["area"] = from_str(self.area)
        result["studyType"] = from_str(self.study_type)
        result["startDate"] = self.start_date.isoformat()
        result["endDate"] = self.end_date.isoformat()
        result["score"] = from_str(self.score)
        result["courses"] = from_list(from_str, self.courses)
        return result


class Interest:
    name: str
    keywords: List[str]

    def __init__(self, name: str, keywords: List[str]) -> None:
        self.name = name
        self.keywords = keywords

    @staticmethod
    def from_dict(obj: Any) -> 'Interest':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        keywords = from_list(from_str, obj.get("keywords"))
        return Interest(name, keywords)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["keywords"] = from_list(from_str, self.keywords)
        return result


class Language:
    language: str
    fluency: str

    def __init__(self, language: str, fluency: str) -> None:
        self.language = language
        self.fluency = fluency

    @staticmethod
    def from_dict(obj: Any) -> 'Language':
        assert isinstance(obj, dict)
        language = from_str(obj.get("language"))
        fluency = from_str(obj.get("fluency"))
        return Language(language, fluency)

    def to_dict(self) -> dict:
        result: dict = {}
        result["language"] = from_str(self.language)
        result["fluency"] = from_str(self.fluency)
        return result


class Project:
    name: str
    description: str
    highlights: List[str]
    keywords: List[str]
    start_date: datetime
    end_date: datetime
    url: str
    roles: List[str]
    entity: str
    type: str

    def __init__(self, name: str, description: str, highlights: List[str], keywords: List[str], start_date: datetime, end_date: datetime, url: str, roles: List[str], entity: str, type: str) -> None:
        self.name = name
        self.description = description
        self.highlights = highlights
        self.keywords = keywords
        self.start_date = start_date
        self.end_date = end_date
        self.url = url
        self.roles = roles
        self.entity = entity
        self.type = type

    @staticmethod
    def from_dict(obj: Any) -> 'Project':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        description = from_str(obj.get("description"))
        highlights = from_list(from_str, obj.get("highlights"))
        keywords = from_list(from_str, obj.get("keywords"))
        start_date = from_datetime(obj.get("startDate"))
        end_date = from_datetime(obj.get("endDate"))
        url = from_str(obj.get("url"))
        roles = from_list(from_str, obj.get("roles"))
        entity = from_str(obj.get("entity"))
        type = from_str(obj.get("type"))
        return Project(name, description, highlights, keywords, start_date, end_date, url, roles, entity, type)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["description"] = from_str(self.description)
        result["highlights"] = from_list(from_str, self.highlights)
        result["keywords"] = from_list(from_str, self.keywords)
        result["startDate"] = self.start_date.isoformat()
        result["endDate"] = self.end_date.isoformat()
        result["url"] = from_str(self.url)
        result["roles"] = from_list(from_str, self.roles)
        result["entity"] = from_str(self.entity)
        result["type"] = from_str(self.type)
        return result


class Publication:
    name: str
    publisher: str
    release_date: datetime
    url: str
    summary: str

    def __init__(self, name: str, publisher: str, release_date: datetime, url: str, summary: str) -> None:
        self.name = name
        self.publisher = publisher
        self.release_date = release_date
        self.url = url
        self.summary = summary

    @staticmethod
    def from_dict(obj: Any) -> 'Publication':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        publisher = from_str(obj.get("publisher"))
        release_date = from_datetime(obj.get("releaseDate"))
        url = from_str(obj.get("url"))
        summary = from_str(obj.get("summary"))
        return Publication(name, publisher, release_date, url, summary)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["publisher"] = from_str(self.publisher)
        result["releaseDate"] = self.release_date.isoformat()
        result["url"] = from_str(self.url)
        result["summary"] = from_str(self.summary)
        return result


class Reference:
    name: str
    reference: str

    def __init__(self, name: str, reference: str) -> None:
        self.name = name
        self.reference = reference

    @staticmethod
    def from_dict(obj: Any) -> 'Reference':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        reference = from_str(obj.get("reference"))
        return Reference(name, reference)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["reference"] = from_str(self.reference)
        return result


class Skill:
    name: str
    level: str
    keywords: List[str]

    def __init__(self, name: str, level: str, keywords: List[str]) -> None:
        self.name = name
        self.level = level
        self.keywords = keywords

    @staticmethod
    def from_dict(obj: Any) -> 'Skill':
        assert isinstance(obj, dict)
        name = from_str(obj.get("name"))
        level = from_str(obj.get("level"))
        keywords = from_list(from_str, obj.get("keywords"))
        return Skill(name, level, keywords)

    def to_dict(self) -> dict:
        result: dict = {}
        result["name"] = from_str(self.name)
        result["level"] = from_str(self.level)
        result["keywords"] = from_list(from_str, self.keywords)
        return result


class Volunteer:
    organization: Optional[str]
    position: str
    url: str
    start_date: datetime
    end_date: datetime
    summary: str
    highlights: List[str]
    name: Optional[str]

    def __init__(self, organization: Optional[str], position: str, url: str, start_date: datetime, end_date: datetime, summary: str, highlights: List[str], name: Optional[str]) -> None:
        self.organization = organization
        self.position = position
        self.url = url
        self.start_date = start_date
        self.end_date = end_date
        self.summary = summary
        self.highlights = highlights
        self.name = name

    @staticmethod
    def from_dict(obj: Any) -> 'Volunteer':
        assert isinstance(obj, dict)
        organization = from_union([from_str, from_none], obj.get("organization"))
        position = from_str(obj.get("position"))
        url = from_str(obj.get("url"))
        start_date = from_datetime(obj.get("startDate"))
        end_date = from_datetime(obj.get("endDate"))
        summary = from_str(obj.get("summary"))
        highlights = from_list(from_str, obj.get("highlights"))
        name = from_union([from_str, from_none], obj.get("name"))
        return Volunteer(organization, position, url, start_date, end_date, summary, highlights, name)

    def to_dict(self) -> dict:
        result: dict = {}
        result["organization"] = from_union([from_str, from_none], self.organization)
        result["position"] = from_str(self.position)
        result["url"] = from_str(self.url)
        result["startDate"] = self.start_date.isoformat()
        result["endDate"] = self.end_date.isoformat()
        result["summary"] = from_str(self.summary)
        result["highlights"] = from_list(from_str, self.highlights)
        result["name"] = from_union([from_str, from_none], self.name)
        return result


class Resume:
    basics: Basics
    work: List[Volunteer]
    volunteer: List[Volunteer]
    education: List[Education]
    awards: List[Award]
    publications: List[Publication]
    skills: List[Skill]
    languages: List[Language]
    interests: List[Interest]
    references: List[Reference]
    projects: List[Project]

    def __init__(self, basics: Basics, work: List[Volunteer], volunteer: List[Volunteer], education: List[Education], awards: List[Award], publications: List[Publication], skills: List[Skill], languages: List[Language], interests: List[Interest], references: List[Reference], projects: List[Project]) -> None:
        self.basics = basics
        self.work = work
        self.volunteer = volunteer
        self.education = education
        self.awards = awards
        self.publications = publications
        self.skills = skills
        self.languages = languages
        self.interests = interests
        self.references = references
        self.projects = projects

    @staticmethod
    def from_dict(obj: Any) -> 'Resume':
        assert isinstance(obj, dict)
        basics = Basics.from_dict(obj.get("basics"))
        work = from_list(Volunteer.from_dict, obj.get("work"))
        volunteer = from_list(Volunteer.from_dict, obj.get("volunteer"))
        education = from_list(Education.from_dict, obj.get("education"))
        awards = from_list(Award.from_dict, obj.get("awards"))
        publications = from_list(Publication.from_dict, obj.get("publications"))
        skills = from_list(Skill.from_dict, obj.get("skills"))
        languages = from_list(Language.from_dict, obj.get("languages"))
        interests = from_list(Interest.from_dict, obj.get("interests"))
        references = from_list(Reference.from_dict, obj.get("references"))
        projects = from_list(Project.from_dict, obj.get("projects"))
        return Resume(basics, work, volunteer, education, awards, publications, skills, languages, interests, references, projects)

    def to_dict(self) -> dict:
        result: dict = {}
        result["basics"] = to_class(Basics, self.basics)
        result["work"] = from_list(lambda x: to_class(Volunteer, x), self.work)
        result["volunteer"] = from_list(lambda x: to_class(Volunteer, x), self.volunteer)
        result["education"] = from_list(lambda x: to_class(Education, x), self.education)
        result["awards"] = from_list(lambda x: to_class(Award, x), self.awards)
        result["publications"] = from_list(lambda x: to_class(Publication, x), self.publications)
        result["skills"] = from_list(lambda x: to_class(Skill, x), self.skills)
        result["languages"] = from_list(lambda x: to_class(Language, x), self.languages)
        result["interests"] = from_list(lambda x: to_class(Interest, x), self.interests)
        result["references"] = from_list(lambda x: to_class(Reference, x), self.references)
        result["projects"] = from_list(lambda x: to_class(Project, x), self.projects)
        return result


def resume_from_dict(s: Any) -> Resume:
    return Resume.from_dict(s)


def resume_to_dict(x: Resume) -> Any:
    return to_class(Resume, x)
