from lxml import etree

import xmltodict

from resume.resume_types import Resume


class InvalidFileStructureError(Exception):
    pass


def convert_to_xml(resume: Resume, output: str):
    data = resume.to_dict()
    data = {'resume': data}
    with open(output, 'w+') as f:
        f.write(xmltodict.unparse(data))
    xmlschema_doc = etree.parse('./schemas/resume-schema.xsd')
    xmlschema = etree.XMLSchema(xmlschema_doc)
    xml_doc = etree.parse(output)
    if not xmlschema.validate(xml_doc):
        raise InvalidFileStructureError('XML does not match provided schema')

