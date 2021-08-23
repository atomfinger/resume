import datetime
import uuid as uuid

import pytz
from icalendar import Calendar, Event, vCalAddress, vText, vDatetime

from resume.resume_types import Resume

WINDOWS_LINE_ENDING = b'\r\n'
UNIX_LINE_ENDING = b'\n'


def convert_to_ics(resume: Resume, destination: str):
    cal = Calendar()
    cal.add('version', '2.0')
    cal.add('prodid', '-//John\'s cheeky calendar thing/jmgundersen.com//')
    cal.add_component(get_event(resume))
    with open(destination, 'wb') as f:
        f.write(cal.to_ical())
    replace_endings(destination)


def get_event(resume: Resume) -> Event:
    event = Event()
    event.add('summary', f'Read {resume.basics.name}\' resume')
    event.add('dtstart', vDatetime(get_event_start()))
    event.add('dtend', vDatetime(get_event_end()))
    event.add('dtstamp', vDatetime(get_event_timestamp()))
    event['locations'] = vText('Somewhere comfortable')
    event['uid'] = str(uuid.uuid4())
    event['organizer'] = get_organizer(resume)
    event.add('attendee', get_attendee(), encode=0)
    event.add('priority', 5)
    event.add('description', get_description(resume))
    return event


def get_organizer(resume: Resume) -> vCalAddress:
    organizer = vCalAddress('MAILTO:john@jmgundersen.com')
    organizer.params['cn'] = vText(resume.basics.name)
    organizer.params['ROLE'] = vText(resume.basics.label)
    return organizer


def get_attendee() -> vCalAddress:
    attendee = vCalAddress('MAILTO:you@somecompany.com')
    attendee.params['cn'] = vText('A person')
    attendee.params['ROLE'] = vText('REQ-PARTICIPANT')
    return attendee


def get_event_start() -> datetime:
    event_date = datetime.date.today() + datetime.timedelta(days=1)
    return datetime.datetime.combine(event_date, datetime.time(13, 37)).replace(tzinfo=pytz.utc)


def get_event_end() -> datetime:
    return (get_event_start() + datetime.timedelta(hours=1)).replace(tzinfo=pytz.utc)


def get_event_timestamp() -> datetime:
    return (datetime.datetime.now() + datetime.timedelta(days=1)).replace(tzinfo=pytz.utc)


def replace_endings(file_path: str):
    with open(file_path, 'rb') as open_file:
        content = open_file.read()

        content = content.replace(WINDOWS_LINE_ENDING, UNIX_LINE_ENDING)

    with open(file_path, 'wb') as open_file:
        open_file.write(content)


def get_description(resume: Resume):
    return f'You should read {resume.basics.name}\'s resume.\n\n' \
           f'The online version can be found here:\n' \
           f'https://atomfinger.github.io/resume/\n\n' \
           f'Other formats are available here:\n' \
           f'https://github.com/atomfinger/resume/releases/latest/\n\n' \
           f'Then you should consider contacting him at {resume.basics.email} ' \
           f'or through his website ({resume.basics.url})'
