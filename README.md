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
| DOCX  | For those who believes in legacy and proprietary formats  | N/A |
| Markdown  | For you with style and class | N/A |
| XML  | Why would you want this?  | [Schema](schemas/resume-schema.xsd)  |
| YAML  | I mean... okay.. but again why?  | [Schema](https://jsonresume.org/schema/) |
| TXT  | Pure text when nothing else works  | N/A |
| CSV  | If XML wasn't legacy enough | Don't want to |
| JPG  | Maybe you're on a device that can only view images. I'm not judging. | Don't want to |

## Where to download/View this resume

If you are one of those who prefer other, lesser, file formats feel free to view the latest
version [online](https://atomfinger.github.io/resume/), or you can download all the other
formats [here](https://github.com/atomfinger/resume/releases/latest/).

If no format exists that support your needs, do let me know :)