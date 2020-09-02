
import re


def isEmptyLine(line):
    return not line.strip()


def matchMarkupCharacter(line, markupCharacter):
    return isEmptyLine(line.replace(markupCharacter, ""))


def isMarkupLine(line):
    for markupCharacter in markupCharacters:
        if matchMarkupCharacter(line, markupCharacter):
            return True
    return False


def isTitleMarkup(line):
    return not isEmptyLine(line) and matchMarkupCharacter(line, titleMarkupCharacter)


def isCategoryMarkup(line):
    return not isEmptyLine(line) and matchMarkupCharacter(line, categoryMarkupCharacter)


def isTaglineLine(line):
    p = re.compile('^#{4} ')
    return p.match(line)


def isContactInformationLine(line):
    p = re.compile('^#{6} ')
    return p.match(line)


def parseContactInformation(line):
    return line  # TODO


def parseCategoryContent(content, i, dict):
    if (i == len(content)):
        return {'dictionary': dict, 'index': i}
    line = content[i]
    if (len(content) == i):
        return {'dictionary': dict, 'index': i}
    if isEmptyLine(line):
        return parseCategoryContent(content, i + 1, dict)
    if (i + 1) < len(content) and isMarkupLine(content[i+1]):
        nextLine = content[i + 1]
        if isCategoryMarkup(nextLine):
            return {'dictionary': dict, 'index': i}
    return parseCategoryContent(content, i + 1, dict)


def parseContent(content, i, dict):
    if (i == len(content)):
        return dict
    line = content[i]
    if isEmptyLine(line) or isMarkupLine(line):
        return parseContent(content, i+1, dict)

    if (i + 1) < len(content) and isMarkupLine(content[i+1]):
        nextLine = content[i + 1]
        if isTitleMarkup(nextLine):
            dict["title"] = line
            return parseContent(content, i + 1, dict)
        if isCategoryMarkup(nextLine):
            if not 'categories' in dict.keys():
                dict['categories'] = []
            categoryDict = {'categoryTitle': line}
            result = parseCategoryContent(content, i + 1, categoryDict)
            print(result)
            dict['categories'].append(result['dictionary'])
            return parseContent(content, result['index'], dict)

    if isTaglineLine(line):
        dict['tagline'] = line.replace('#', '').strip()

    if isContactInformationLine(line):
        dict['contactInformation'] = line.replace('#', '').strip()

    return parseContent(content, i+1, dict)


with open('resume.md') as f:
    content = f.readlines()

content = [x.strip() for x in content]

titleMarkupCharacter = '='
categoryMarkupCharacter = '-'
markupCharacters = [titleMarkupCharacter, categoryMarkupCharacter, "_"]

dict = {'resume': {}}
parseContent(content, 0, dict['resume'])

print(dict)
