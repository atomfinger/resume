from pypub.chapter import create_chapter_from_file
from pypub.epub import Epub


def convert_to_epub(origin: str, output: str):
    epub = Epub('Resume')
    chapter = create_chapter_from_file(origin)
    epub.add_chapter(chapter)
    epub.create_epub(output)
