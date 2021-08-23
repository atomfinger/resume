![Build status](https://github.com/atomfinger/resume/actions/workflows/pipeline.yml/badge.svg)
![Calendar status](https://github.com/atomfinger/resume/actions/workflows/update_calendar.yml/badge.svg)

# John's resume

Howdy! Welcome to John's resume... or, well, at least the repository that generates the resume. Look, let's level for a
second: This was supposed to be this funny little thing so that I didn't have to maintain a Google Docs resume, and it
has spiralled into whatever this is.

Nevertheless, I promise you there's a resume here somewhere! You won't be disappointed!

## Why

Most people write a good few resumes throughout their careers, and it is almost always dull. There are different
requirements for formatting, and every new change or addition is an exercise in design, constraint, spelling and
grammar.

As a developer, I felt that our regular resumes are boring. I should resent proprietary file types such as `DOCX` or
whatever format Google Docs uses as a developer.

As a developer, I should embrace standardization and structured data! As a developer, I should facilitate transformation
of data through code!

## How

The base resume is stored as a JSON file ([view here](resume.json)) and uses the schema outlined
by [JSON Resume](https://jsonresume.org/), which is an open standard for structuring Resume data.

When changes to the JSON Resume file happens, it is automatically put through several tests and transformations to
support a wide variety of formats. Some might see this as a brutal violation
of [YAGNI](https://en.wikipedia.org/wiki/You_aren%27t_gonna_need_it), but I have worked in banking and know that
supporting many formats is very important. Yes indeed. I might not need it today, but one day there will be a recruiter
that will only accept [YAML](https://en.wikipedia.org/wiki/YAML) files; just you wait!

## Supported formats

| Format  | Description  | Schema |
|---|---|---|
| JSON  | Resume stored with the schema outlined by [JSON Resume](https://jsonresume.org/) | [Schema](https://jsonresume.org/schema/)  |
| HTML  | Resume to be viewed in a browser  | N/A |
| PDF  | Resume to be viewed in a PDF reader | N/A |
| Markdown  | For you with style and class | N/A |
| XML  | Why would you want this?  | I tried, but it turned into a hassle.  |
| YAML  | I mean... okay.. but again why?  | [Schema](https://jsonresume.org/schema/) |
| TXT  | Pure text when nothing else works  | N/A |
| CSV  | If XML wasn't legacy enough | Don't want to |
| JPG  | Maybe you're on a device that can only view images. I'm not judging. | [Schema](https://jpeg.org/jpeg/workplan.html) |
| Morse code (TXT) | The most legacy format | N/A |
| TIFF | Companies still use FAX machines, right? | N/A |

## Where to download/View this resume

If you are one of those who prefer other, lesser, file formats feel free to view the latest
version [online](https://atomfinger.github.io/resume/), or you can download all the other
formats [here](https://github.com/atomfinger/resume/releases/latest/).

If no format exists that support your needs, do let me know :)

## Build locally

This project uses 3 different technologies for generating the various file types:

- [resume-cli](https://www.npmjs.com/package/resume-cli): The official JSON resume command lined tool.
- Python: For custom transformations not supported by `resume-cli`.
- GitHub Actions: For when there's a quick and easy action that does what I need it to do.

### Resume-CLI

`Resume-CLI` is installed through NPM:

```npm install -g resume-cli```

Then you can execute transformation (while being in the root folder) as such:

```resume export resume.html --format html```

For more information head over to the [official repository](https://github.com/jsonresume/resume-cli).

If you get an error you might have to also install the default theme: `npm install jsonresume-theme-even`

### GitHub Actions

Some formats are only generated through various GitHub Actions. If you want to reproduce them you can always see how
they're executed by going to the [`.github/workflows/` folder](.github/workflows).

### Python

Some formats are dumb, or they don't have a natural way to convert. For these scenarios the application uses Python.

#### How to run

1. You should [start a virtual environment](https://docs.python.org/3/library/venv.html)
2. Install required packages: `pip install -r requirements.txt`
3. Install the python package: `python setup.py install`
4. Run a command, such as `python ./resume/__main__.py --input 'resume.json' --output 'resume.md' --format 'markdown'`

#### How to run tests

The same as above, but instead of running `__main__.py` you use this command `pytest` (needs pytest installed).