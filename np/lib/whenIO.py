'Methods for transforming dates to strings and vice versa'
import datetime
import re


indexByWeekday = {
       'monday': 0, 'mon': 0,
      'tuesday': 1, 'tue': 1,
    'wednesday': 2, 'wed': 2,
     'thursday': 3, 'thu': 3,
       'friday': 4, 'fri': 4,
     'saturday': 5, 'sat': 5,
       'sunday': 6, 'sun': 6,
}
dateTemplates = '%m/%d/%Y', '%m/%d/%y', '%m/%d'
timeTemplates = '%I%p', '%I:%M%p'


class WhenIO(object):
    'Time conversion'
    
    # Constructor

    def __init__(self, minutesOffset=0, localToday=None):
        'Initialize time offset and special dates'
        # Set
        self.minutesOffset = minutesOffset
        self.localToday = localToday.date() if localToday else self.to_local(datetime.datetime.utcnow()).date()
        self.localTomorrow = self.localToday + datetime.timedelta(days=1)
        self.localYesterday = self.localToday + datetime.timedelta(days=-1)

    # Parse

    def parse(self, whensString, toUTC=True):
        """
        Parse whens from strings.
        toUTC=True   Convert whens to UTC after parsing
        toUTC=False  Parse whens without conversion
        """
        # Initialize
        whens, terms = [], []
        # For each term,
        for term in whensString.split():
            # Try to parse the term as a date
            date = self.parse_date(term)
            # If the term is a date,
            if date != None: 
                if date not in whens:
                    whens.append(date)
                continue
            # Try to parse the term as a time
            time = self.parse_time(term)
            # If the term is a time,
            if time != None: 
                # Load
                oldWhen = whens[-1] if whens else self.localToday
                newWhen = self.combine_date_time(oldWhen, time)
                # If oldWhen already has a time or we have no whens, append newWhen
                if isinstance(oldWhen, datetime.datetime) or not whens:
                    whens.append(newWhen)
                # If oldWhen did not have a time, replace oldWhen
                else:
                    whens[-1] = newWhen
                continue
            # If it is neither a date nor a time, save it
            if term not in terms:
                terms.append(term)
        # Make sure every when has a time
        for whenIndex, when in enumerate(whens):
            if not isinstance(when, datetime.datetime):
                whens[whenIndex] = self.combine_date_time(when, whenTime=None)
        # Convert
        if toUTC:
            whens = map(self.from_local, whens)
        # Return
        return sorted(whens), terms

    def parse_date(self, dateString):
        'Parse date from a string'
        # Prepare string
        dateString = dateString.strip().lower()
        # Look for special terms
        if dateString in ('today', 'tod'):
            return self.localToday
        elif dateString in ('tomorrow', 'tom'):
            return self.localTomorrow
        elif dateString in ('yesterday', 'yes'):
            return self.localYesterday
        elif dateString in indexByWeekday:
            difference = indexByWeekday[dateString] - self.localToday.weekday()
            if difference <= 0: 
                difference += 7
            return self.localToday + datetime.timedelta(days=difference)
        # Parse date
        for template in dateTemplates:
            try: 
                date = datetime.datetime.strptime(dateString, template).date()
            except (ValueError, TypeError):
                pass
            else:
                if date.year == 1900:
                    date = date.replace(year=self.localToday.year)
                return date

    def parse_time(self, timeString):
        'Parse time from a string'
        # Prepare string
        timeString = timeString.strip().lower()
        # Parse time
        for template in timeTemplates:
            try: 
                time = datetime.datetime.strptime(timeString, template).time()
            except (ValueError, TypeError):
                pass
            else: 
                return time

    # Format

    def format(self, whens, dateTemplate=dateTemplates[0], dateTemplate_='', fromUTC=True):
        """
        Format whens into strings.
        dateTemplate   Date template to use when the date is more than seven days from today
        dateTemplate_  Date template to use when the date is less than seven days from today
        fromUTC=True   Convert whens to local time before formatting
        fromUTC=False  Format whens without conversion
        """
        # Convert
        if not isinstance(whens, list):
            whens = [whens]
        if fromUTC:
            whens = map(self.to_local, whens)
        # Initialize
        strings = []
        previousDate = None
        # For each when,
        for when in whens:
            # Ignore null
            if when == None: 
                continue
            # If the when matches the previousDate,
            if when.date() == previousDate:
                # Only format time
                string = self.format_time(when)
            # Otherwise,
            else:
                # Format
                string = '%s %s' % (self.format_date(when, dateTemplate, dateTemplate_), self.format_time(when))
            # Append
            strings.append(string)
            # Prepare for next iteration
            previousDate = when.date()
        # Return
        return ' '.join(strings)

    def format_date(self, date, dateTemplate=dateTemplates[0], dateTemplate_=''):
        'Format date into string'
        # Convert
        if isinstance(date, datetime.datetime): 
            date = date.date()
        dateString = date.strftime(dateTemplate_) if dateTemplate_ else ''
        # Format special
        if date == self.localToday: 
            return 'Today' + dateString
        elif date == self.localTomorrow: 
            return 'Tomorrow' + dateString
        elif date == self.localYesterday: 
            return 'Yesterday' + dateString
        # Format weekday
        differenceInDays = (date - self.localToday).days
        if differenceInDays <= 7 and differenceInDays > 0:
            return date.strftime('%A') + dateString
        # Return
        return date.strftime(dateTemplate)

    def format_time(self, time):
        'Format time into string'
        # Convert
        if isinstance(time, datetime.datetime): 
            time = time.time()
        # Format
        hour = time.hour % 12
        if not hour: 
            hour = 12
        hour = str(hour)
        if time.minute == 0: 
            return hour + time.strftime('%p').lower()
        # Return
        return hour + time.strftime(':%M%p').lower()

    def format_offset(self):
        return format_offset(self.minutesOffset)

    # Helpers

    def combine_date_time(self, whenDate, whenTime=None):
        'Create when from date and time, assuming where necessary'
        # If both terms are present, combine them            
        if whenTime != None and whenDate: 
            return datetime.datetime.combine(whenDate, whenTime)
        # If only the time is present,
        if whenTime != None: 
            return datetime.datetime.combine(self.localToday, whenTime)
        # If only the date is present,
        if whenDate: 
            return datetime.datetime.combine(whenDate, datetime.time(0, 0))

    def from_local(self, when):
        'Convert whenLocal into UTC'
        if when:
            return when + datetime.timedelta(minutes=self.minutesOffset)

    def to_local(self, when):
        'Convert UTC into whenLocal'
        if when: 
            return when - datetime.timedelta(minutes=self.minutesOffset)


def format_offset(minutesOffset):
    'Format timezone offset'
    hourCount = minutesOffset / 60.
    hourQuotient = int(hourCount)
    hourRemainder = abs(hourCount - hourQuotient)
    return '%+03d%02d UTC' % (-1 * hourCount, hourRemainder * 60)


def parse_offset(text):
    'Parse timezone offset'
    pattern_offset = re.compile(r'([+-]\d\d)(\d\d) UTC')
    matchOffset = pattern_offset.search(text)
    if matchOffset:
        x, y = matchOffset.groups()
        x = int(x)
        y = int(y)
        minutesOffset = (1 if x < 0 else -1) * (abs(x) * 60 + y)
        text = pattern_offset.sub('', text)
    else:
        minutesOffset = None
    return minutesOffset, text
