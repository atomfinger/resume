import pypub


def convert_to_epub(origin: str, output: str):
    epub = pypub.Epub('Resume')
    chapter = pypub.create_chapter_from_file(origin)
    epub.add_chapter(chapter)
    epub.create_epub(output)
