import argparse
import json
from argparse import Namespace

from resume.json_to_ics import convert_to_ics
from resume.json_to_csv import convert_to_csv
from resume.json_to_md import convert_to_markdown
from resume.json_to_pptx import convert_to_pptx
from resume.json_to_xml import convert_to_xml
from resume.json_to_yaml import convert_to_yaml
from resume.pdf_to_jpg import convert_to_jpg
from resume.resume_types import resume_from_dict
from resume.simplify import simplify
from resume.txt_to_morse_code import convert_to_morse_code


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', metavar='path', type=str, help='Input JSON file', required=True)
    parser.add_argument('--output', metavar='path', type=str, help='Output file', required=True)
    parser.add_argument('--format', type=str,
                        choices=['markdown', 'yaml', 'xml', 'csv', 'jpg', 'morse', 'simplify', 'ics', 'pptx'],
                        required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    file_format = args.format.lower()
    destination = args.output
    source = args.input

    if file_format == 'jpg':
        convert_to_jpg(source, destination)
        return
    if file_format == 'morse':
        convert_to_morse_code(source, destination)
        return
    if file_format == 'simplify':
        simplify(source, destination)
        return

    with open(source, 'r') as f:
        resume = resume_from_dict(json.loads(f.read()))

    if file_format == 'markdown':
        convert_to_markdown(resume, destination)
    elif file_format == 'yaml':
        convert_to_yaml(resume, destination)
    elif file_format == 'xml':
        convert_to_xml(resume, destination)
    elif file_format == 'csv':
        convert_to_csv(args.input, destination)
    elif file_format == 'jpg':
        convert_to_jpg(args.input, destination)
    elif file_format == 'ics':
        convert_to_ics(resume, destination)
    elif file_format == 'pptx':
        convert_to_pptx(resume, destination)
    else:
        raise ValueError(f'{args.format} is not a supported format')


if __name__ == '__main__':
    main()
