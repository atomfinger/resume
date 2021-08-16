import argparse
import json
from argparse import Namespace
from typing import Optional

from resume.json_to_md import convert_to_markdown
from resume.json_to_yaml import convert_to_yaml
from resume.resume_types import resume_from_dict


def parse_arguments() -> Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', metavar='path', type=str, help='Input JSON file', required=True)
    parser.add_argument('--output', metavar='path', type=str, help='Output file', required=True)
    parser.add_argument('--format', type=str, choices=['markdown', 'yaml'], required=True)
    return parser.parse_args()


def main():
    args = parse_arguments()
    new_file_content: Optional[str] = None
    with open(args.input, 'r') as f:
        resume = resume_from_dict(json.loads(f.read()))
    if args.format.lower() == 'markdown':
        new_file_content = convert_to_markdown(resume)
    elif args.format.lower() == 'yaml':
        convert_to_yaml(resume, args.output)
    else:
        raise ValueError(f'{args.format} is not a supported format')
    if new_file_content:
        with open(args.output, 'w+') as f:
            f.write(new_file_content)


if __name__ == '__main__':
    main()
