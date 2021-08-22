import argparse
import json
from argparse import Namespace

from resume.json_to_csv import convert_to_csv
from resume.json_to_md import convert_to_markdown
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
    parser.add_argument('--format', type=str, choices=['markdown', 'yaml', 'xml', 'csv', 'jpg', 'morse', 'simplify'],
                        required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    if args.format.lower() == 'jpg':
        convert_to_jpg(args.input, args.output)
        return
    if args.format.lower() == 'morse':
        convert_to_morse_code(args.input, args.output)
        return
    if args.format.lower() == 'simplify':
        simplify(args.input, args.output)
        return
    with open(args.input, 'r') as f:
        resume = resume_from_dict(json.loads(f.read()))
    if args.format.lower() == 'markdown':
        convert_to_markdown(resume, args.output)
    elif args.format.lower() == 'yaml':
        convert_to_yaml(resume, args.output)
    elif args.format.lower() == 'xml':
        convert_to_xml(resume, args.output)
    elif args.format.lower() == 'csv':
        convert_to_csv(args.input, args.output)
    elif args.format.lower() == 'jpg':
        convert_to_jpg(args.input, args.output)
    else:
        raise ValueError(f'{args.format} is not a supported format')


if __name__ == '__main__':
    main()
