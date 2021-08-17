import xmltodict

from resume.resume_types import Resume


class InvalidFileStructureError(Exception):
    pass


def convert_to_xml(resume: Resume, output: str):
    data = resume.to_dict()
    data = {'resume': data}
    with open(output, 'w+') as f:
        f.write(xmltodict.unparse(data))
