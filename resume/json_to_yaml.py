import ruamel.yaml

from resume.resume_types import Basics, Resume, Volunteer, Education, Skill, Award, Publication, Language, Interest, \
    Project, Reference, Profile, Work


def convert_to_yaml(resume: Resume, destination: str):
    yaml = ruamel.yaml.YAML()
    resume_types = [Basics, Resume, Volunteer, Education, Skill, Award, Publication, Language, Interest, Project,
                    Reference, Profile, Work]
    [yaml.register_class(resume_type) for resume_type in resume_types]
    with open(destination, 'w+') as f:
        yaml.dump(resume, f)
