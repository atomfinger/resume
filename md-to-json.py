import re
from enum import Enum
import sys
import json


#
#   CLASS DEFINITIONS
#


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


#
#   DUMB PARSING PURE TEXT
#


def parseListLine(line):
    return line.replace("*", "").strip()


def parseEducationLine(line):
    arr = line.split('**,')
    schoolAndDates = arr[1].split("(")
    dates = schoolAndDates[1].split("-")
    return {
        "degree": arr[0].replace("*", "").strip(),
        'institution': schoolAndDates[0].strip(),
        'started': dates[0].strip(),
        'graduated': dates[1].replace(")", "").strip()
    }


def parseExperienceHeadingLine(line):
    arr = line.split('**,')
    schoolAndDates = arr[1].split("(")
    dates = schoolAndDates[1].split("-")
    return {
        "title": arr[0].replace("*", "").strip(),
        'employer': schoolAndDates[0].strip(),
        'start': dates[0].strip(),
        'end': dates[1].replace(")", "").strip()
    }


def parseSkillsLine(line):
    arr = line.split(":**")
    return {
        'skillCategory': arr[0].replace("*", "").strip(),
        'skills': [x.strip() for x in arr[1].split(",")]
    }


def parseTitleLines(line):
    return line.replace("#", "").strip()


def parseContactLine(line):
    list = []
    arr = parseTitleLines(line).split("-")
    for contact in arr:
        if "](" in contact:
            list.append(contact.split("](")[1].strip(")").strip())
        else:
            list.append(contact.strip())
    return list


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


#
#   READERS
#


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
        if lineType is LineType.SUBSECTION_TITLE:
            experienceInfo = parseExperienceHeadingLine(value)
            dict['title'] = experienceInfo['title']
            dict['employer'] = experienceInfo['employer']
            dict['start'] = experienceInfo['start']
            dict['end'] = experienceInfo['end']
        if lineType is LineType.TEXT:
            dict['description'] = value
        if lineType is LineType.LIST:
            if 'responsibilities' not in dict.keys():
                dict['responsibilities'] = []
            dict['responsibilities'].append(
                {'description': parseListLine(value)})
        if lineType is LineType.SUBLIST:
            if 'clarifications' not in dict['responsibilities'][-1].keys():
                dict['responsibilities'][-1]['clarifications'] = []
            dict['responsibilities'][-1]['clarifications'].append(
                parseListLine(value))
    return dict


def readEducations(content, indexFrom, indexTo):
    list = []
    for i in range(indexFrom, indexTo):
        line = content[i]
        lineType = line['type']
        value = line['value']
        if lineType != LineType.SUBSECTION_TITLE:
            continue
        list.append(parseEducationLine(value))
    return list


def readSkills(content, indexFrom, indexTo):
    list = []
    for i in range(indexFrom, indexTo):
        line = content[i]
        lineType = line['type']
        value = line['value']
        if lineType != LineType.SUBSECTION_TITLE:
            continue
        list.append(parseSkillsLine(value))
    return list


def readOther(content, indexFrom, indexTo):
    list = []
    for i in range(indexFrom, indexTo):
        line = content[i]
        lineType = line['type']
        value = line['value']
        if lineType != LineType.LIST:
            continue
        list.append(parseListLine(value))
    return list


def readSection(content, indexFrom):
    line = parsedContent[indexFrom]
    lineType = line['type']
    value = line['value']
    nextSectionIndex = getNextSectionIndex(parsedContent, indexFrom + 1)
    if value.lower() == 'experience':
        result = readExperiences(parsedContent, indexFrom, nextSectionIndex)
    elif value.lower() == 'education':
        result = readEducations(parsedContent, indexFrom, nextSectionIndex)
    elif value.lower() == 'skills':
        result = readSkills(parsedContent, indexFrom, nextSectionIndex)
    elif value.lower() == 'other':
        result = readOther(parsedContent, indexFrom, nextSectionIndex)
    else:
        raise Exception("Unsupported section type: " + value)
    return {
        'title': value.lower(),
        'value': result
    }


#
# NIFTY HELPER FUNCTIONS
#


def categorizeLine(line):
    map = getLineTypeMap()
    for key in map.keys():
        if re.compile(map[key]).match(line):
            return key
    if not line.strip():
        return LineType.NOTHING
    return LineType.UNKNOWN


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


def generateJson(content):
    dict = {}
    for i in range(len(content)):
        line = content[i]
        lineType = line['type']
        value = line['value']

        if lineType is LineType.TITLE:
            dict['title'] = value
        if lineType is LineType.SUBTITLE:
            dict['subtitle'] = parseTitleLines(value)
        if lineType is LineType.CONTACT:
            dict['contact'] = parseContactLine(value)

        if lineType is LineType.SECTION:
            result = readSection(content, i)
            dict[result['title']] = result['value']
    return dict


file = sys.argv[1]
with open(file) as f:
    content = f.readlines()
parsedContent = [x for x in parseContent(content) if (
    x['type'] != LineType.NOTHING and x['type'] != LineType.UNKNOWN
)]
dict = generateJson(parsedContent)
json_string = json.dumps(dict, ensure_ascii=False).encode('utf8')
print(json_string.decode())
sys.exit(0)
