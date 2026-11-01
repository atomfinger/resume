import json


def simplify(origin: str, destination: str):
    """The short version of the resume, for the PDF and the images made from it.

    Optional sections are removed rather than set to null, so the result is still valid against the schema."""
    with open(origin, 'r') as f:
        resume = json.loads(f.read())
    resume['basics'].pop('location', None)
    resume.pop('interests', None)
    # My own projects are dropped, but the talks (projects of type "talk") stay.
    talks = [with_single_date(project) for project in resume.get('projects') or [] if project.get('type') == 'talk']
    if talks:
        resume['projects'] = talks
    else:
        resume.pop('projects', None)
    resume['education'] = [resume['education'][0]]
    with open(destination, 'w+') as f:
        f.write(json.dumps(resume))


def with_single_date(talk: dict) -> dict:
    """A talk happens on one date: without an end date the theme would show a range that ends in "Present"."""
    result = dict(talk)
    if 'startDate' in result:
        result['endDate'] = result['startDate']
    return result
