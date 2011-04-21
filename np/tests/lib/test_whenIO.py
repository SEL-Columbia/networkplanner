'Tests for whenIO'
import datetime

from np.lib import whenIO


# Setup
localWhenIO = whenIO.WhenIO()
localToday = localWhenIO.localToday
localTomorrow = localWhenIO.localTomorrow
localYesterday = localWhenIO.localYesterday


def test_parse():
    'Test that parsing works properly'
    # Define
    def assertParse(whenString, when):
        assert localWhenIO.parse(whenString, toUTC=False)[0][0] == when
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


def test_format():
    'Test that formatting works properly'
    # Define
    def assertFormat(when, whenString):
        assert localWhenIO.parse(whenString, toUTC=False)[0][0] == whenExpected
    # Test %m/%d/%y
    assert localWhenIO.format_date(datetime.date(2009, 5, 10), dateTemplate='%m/%d/%y') == '05/10/09'
    # Test %m/%d/%Y %H:%M%p
    assert localWhenIO.format(datetime.datetime(2009, 5, 10, 15, 2), dateTemplate='%m/%d/%Y') == '05/10/2009 3:02pm'


def test_offset():
    'Test that we can format and parse offset properly'
    # Format
    assert whenIO.format_offset(-765) == '+1245 UTC'
    assert whenIO.format_offset(-540) == '+0900 UTC'
    assert whenIO.format_offset(-390) == '+0630 UTC'
    assert whenIO.format_offset(-270) == '+0430 UTC'
    assert whenIO.format_offset(   0) == '+0000 UTC'
    assert whenIO.format_offset(+240) == '-0400 UTC'
    assert whenIO.format_offset(+270) == '-0430 UTC'
    assert whenIO.format_offset(+360) == '-0600 UTC'
    # Parse
    assert whenIO.parse_offset('+1245 UTC')[0] == -765
    assert whenIO.parse_offset('+0900 UTC')[0] == -540
    assert whenIO.parse_offset('+0630 UTC')[0] == -390
    assert whenIO.parse_offset('+0430 UTC')[0] == -270
    assert whenIO.parse_offset('+0000 UTC')[0] ==    0
    assert whenIO.parse_offset('-0400 UTC')[0] == +240
    assert whenIO.parse_offset('-0430 UTC')[0] == +270
    assert whenIO.parse_offset('-0600 UTC')[0] == +360
