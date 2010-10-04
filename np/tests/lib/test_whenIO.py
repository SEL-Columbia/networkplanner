'Tests for whenIO'
# Import system modules
import datetime
import random
# Import custom modules
from np.lib import whenIO


# Setup
localWhenIO = whenIO.WhenIO()
localToday = localWhenIO.localToday
localTomorrow = localWhenIO.localTomorrow
localYesterday = localWhenIO.localYesterday


def test_parse_single():
    # Define
    def assertParse(whenString, when):
        assert localWhenIO.parse(whenString, withConversion=False)[0][0] == when
    # Test %m/%d/%y
    assertParse('5/21/09', datetime.datetime(2009, 5, 21, 0, 0))
    # Test %m/%d/%Y
    assertParse('5/21/2009', datetime.datetime(2009, 5, 21, 0, 0))
    # Test %m/%d/%Y %H%p
    assertParse('5/21/2009 3pm', datetime.datetime(2009, 5, 21, 15, 0))
    # Test %m/%d/%Y %H:%M%p
    assertParse('5/21/2009 3:15pm', datetime.datetime(2009, 5, 21, 15, 15))
    # Test special dates
    assertParse('today 1pm', datetime.datetime.combine(localToday, datetime.time(13, 0)))
    assertParse('tomorrow 12am', datetime.datetime.combine(localTomorrow, datetime.time(0, 0)))
    assertParse('yesterday 12:30pm', datetime.datetime.combine(localYesterday, datetime.time(12, 30)))


def test_format_single():
    # Define
    def assertFormat(when, whenString):
        assert localWhenIO.parse(whenString, withConversion=False)[0][0] == whenExpected
    # Test %m/%d/%y
    assert localWhenIO.formatDate(datetime.date(2009, 5, 10), dateTemplate='%m/%d/%y') == '05/10/09'
    # Test %m/%d/%Y %H:%M%p
    assert localWhenIO.format(datetime.datetime(2009, 5, 10, 15, 2), dateTemplate='%m/%d/%Y') == '05/10/2009 3:02pm'
