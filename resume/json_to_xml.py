import xmltodict

from resume.resume_types import Resume


def convert_to_xml(resume: Resume) -> str:
    data = resume.to_dict()
    data = {'resume': data}
    return xmltodict.unparse(data)
