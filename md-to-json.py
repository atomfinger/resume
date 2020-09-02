
import re
from enum import Enum


def isEmptyLine(line):
    return not line.strip()


def matchMarkupCharacter(line, markupCharacter):
    return isEmptyLine(line.replace(markupCharacter, ""))


def isMarkupLine(line):
    markupLineTypes = [
        LineType.TITLE,
        LineType.SECTION,
    ]
    map = getLineTypeMap()
    for key in map.keys():
        if key in markupLineTypes and re.compile(map[key]).match(line):
            return True
    return False


class SectionTypes(Enum):
    EXPERIENCE = 1
    EDUCATION = 2
    SKILLS = 3
    OTHER = 4


class LineType(Enum):
    TITLE = 1
    SUBTITLE = 2
    CONTACT = 3
    SECTION = 4
    SUBSECTION_TITLE = 5
    LIST = 7
    SUBLIST = 8
    TEXT = 9
    NOTHING = 98
    UNKNOWN = 99


def getLineTypeMap():
    return {
        LineType.TITLE: "^={1,} *$",
        LineType.SUBTITLE: "^#{4} .*$",
        LineType.CONTACT: "^#{6} .*$",
        LineType.SECTION: "^-{1,} *$",
        LineType.SUBSECTION_TITLE: "^\*{2}(.*(\)))|(\*{2}.*)$",
        LineType.LIST: "^ \* .*",
        LineType.SUBLIST: "^( ){4,}\* .*",
        LineType.TEXT: "^.{1,}$"
    }


def readExperiences(content, indexFrom, indexTo):
    list = []
    for i in range(indexFrom, indexTo):
        line = content[i]
        lineType = line['type']
        value = line['value']
        if lineType is LineType.SUBSECTION_TITLE:
            nextSubSectionTitle = getNextSubsectionTitleIndex(content, i + 1)
            list.append(readExperience(content, i, nextSubSectionTitle))
    return list


def readExperience(content, indexFrom, indexTo):
    dict = {}
    for i in range(indexFrom, indexTo):
        line = content[i]
        lineType = line['type']
        value = line['value']
        if lineType is LineType.NOTHING or lineType is LineType.UNKNOWN:
            continue
        if lineType is LineType.SUBSECTION_TITLE:
            dict['title'] = value
        if lineType is LineType.TEXT:
            dict['description'] = value
    return dict


def categorizeLine(line):
    map = getLineTypeMap()
    for key in map.keys():
        if re.compile(map[key]).match(line):
            return key
    if not line.strip():
        return LineType.NOTHING
    return LineType.UNKNOWN


def parseContent(content):
    lines = []
    for i in range(len(content)):
        line = content[i]
        lineToCategorize = line
        if i+1 < len(content) and isMarkupLine(content[i+1]):
            lineToCategorize = content[i+1]
        category = categorizeLine(lineToCategorize)
        if isMarkupLine(line):
            category = LineType.NOTHING
        lines.append({
            "value": line.strip(),
            "type": category
        })
    return lines


def getNextSubsectionTitleIndex(content, currentIndex):
    return getNextLineTypeSection(content, currentIndex, LineType.SUBSECTION_TITLE)


def getNextSectionIndex(content, currentIndex):
    return getNextLineTypeSection(content, currentIndex, LineType.SECTION)


def getNextLineTypeSection(content, currentIndex, lineType):
    if currentIndex == len(content):
        return currentIndex
    if content[currentIndex]['type'] == lineType:
        return currentIndex
    return getNextLineTypeSection(content, currentIndex+1, lineType)


with open('resume.md') as f:
    content = f.readlines()

content = content

dict = {}
parsedContent = parseContent(content)

for i in range(len(parsedContent)):
    line = parsedContent[i]
    lineType = line['type']
    value = line['value']
    if lineType is LineType.NOTHING or lineType is LineType.UNKNOWN:
        continue

    if lineType is LineType.TITLE:
        dict['title'] = value
    if lineType is LineType.SUBTITLE:
        dict['subtitle'] = value
    if lineType is LineType.CONTACT:
        dict['contact'] = value

    if lineType is LineType.SECTION:
        nextSectionIndex = getNextSectionIndex(parsedContent, i + 1)
        if value.lower() == 'experience':
            dict['experience'] = readExperiences(parsedContent, i, nextSectionIndex)

print(dict)
