# vim: set fileencoding=UTF-8
from datetime import timedelta

from django.test import SimpleTestCase
from django.core.exceptions import ValidationError

from .fields import NaturalDurationField


class NaturalDurationFieldTest(SimpleTestCase):
    f = NaturalDurationField()
    robo_f = NaturalDurationField(False)
    human_f = NaturalDurationField(True)

    def introspect(self, delta):
        self.assertEquals(delta, self.f.to_python(
            self.human_f.prepare_value(delta))
        )
        self.assertEquals(delta, self.f.to_python(
            self.robo_f.prepare_value(delta))
        )

    def test_decimal(self):
        base = timedelta(hours=6, minutes=30)
        self.assertEquals(base, self.f.to_python("6.5 hours"))
        self.introspect(base)
        base = timedelta(seconds=6, milliseconds=500)
        self.assertEquals(base, self.f.to_python("6.5 seconds"))
        # decimals implemented as float of seconds, so testing here
        self.introspect(base)

    def test_bad_input(self):
        self.assertRaises(ValidationError, self.f.to_python, "asjdfsav")
        self.assertRaises(ValidationError, self.f.to_python, "as1minjdfsav")
        self.assertRaises(ValidationError, self.f.to_python, u"asµjdfsav")

    def test_combo(self):
        base = timedelta(hours=6, minutes=35)
        self.assertEquals(base, self.f.to_python("6 hours 35 minutes"))
        self.assertEquals(base, self.f.to_python("6 hours, 35 minutes"))
        self.assertEquals(base, self.f.to_python("6 hours and 35 minutes"))
        self.assertEquals(base, self.f.to_python("6 hours & 35 minutes"))
        self.assertEquals(base, self.f.to_python("6 h35 minutes"))
        self.introspect(base)
        base = timedelta(hours=6, minutes=35, seconds=30)
        self.assertEquals(base,
                          self.f.to_python("6 hours 35 minutes 30 seconds"))
        self.assertEquals(base,
                          self.f.to_python("6 hours35 minutes and 30 seconds"))
        self.introspect(base)

    def test_micro(self):
        base = timedelta(microseconds=1)
        self.assertEquals(base, self.f.to_python('1 microsecond'))
        self.assertEquals(base, self.f.to_python('1 micro'))
        self.assertEquals(base, self.f.to_python('1 mic'))
        self.assertEquals(base, self.f.to_python('1 us'))
        self.assertEquals(base, self.f.to_python('1 u'))
        self.assertEquals(base, self.f.to_python(u'1 µs'))
        self.assertEquals(base, self.f.to_python(u'1 µ'))
        self.introspect(base)

    def test_millis(self):
        base = timedelta(milliseconds=1)
        self.assertEquals(base, self.f.to_python('1 millisecond'))
        self.assertEquals(base, self.f.to_python('1 mil'))
        self.assertEquals(base, self.f.to_python('1 ms'))
        self.introspect(base)

    def test_second(self):
        base = timedelta(seconds=1)
        self.assertEquals(base, self.f.to_python('1 second'))
        self.assertEquals(base, self.f.to_python('1 sec'))
        self.assertEquals(base, self.f.to_python('1 s'))
        self.introspect(base)

    def test_minute(self):
        base = timedelta(minutes=1)
        self.assertEquals(base, self.f.to_python('1 minute'))
        self.assertEquals(base, self.f.to_python('1 min'))
        self.assertEquals(base, self.f.to_python('1 m'))
        self.assertNotEquals(base, self.f.to_python('1 ms'))
        self.introspect(base)

    def test_hour(self):
        base = timedelta(hours=1)
        self.assertEquals(base, self.f.to_python('1 hour'))
        self.assertEquals(base, self.f.to_python('1 hr'))
        self.assertEquals(base, self.f.to_python('1 h'))
        self.introspect(base)

    def test_day(self):
        base = timedelta(days=1)
        self.assertEquals(base, self.f.to_python('1 day'))
        self.assertEquals(base, self.f.to_python('1 dy'))
        self.assertEquals(base, self.f.to_python('1 d'))
        self.introspect(base)

    def test_week(self):
        base = timedelta(days=7)
        self.assertEquals(base, self.f.to_python('1 week'))
        self.assertEquals(base, self.f.to_python('1 wk'))
        self.assertEquals(base, self.f.to_python('1 w'))
        self.introspect(base)

    def test_month(self):
        base = timedelta(days=60)
        self.assertEquals(base, self.f.to_python('2 months'))
        self.assertEquals(base, self.f.to_python('2 mo'))
        self.assertEquals(base, self.f.to_python('2 mos'))
        self.introspect(base)

    def test_year(self):
        base = timedelta(days=365)
        self.assertEquals(base, self.f.to_python('1 year'))
        self.introspect(base)
        base = timedelta(days=365 * 10)
        self.assertEquals(base, self.f.to_python('10 years'))
        self.introspect(base)

    def test_a(self):
        base = timedelta(hours=1)
        self.assertEquals(base, self.f.to_python('an hour'))
        self.introspect(base)
        base = timedelta(minutes=1)
        self.assertEquals(base, self.f.to_python('a minute'))
        self.introspect(base)

    def test_null(self):
        self.assertIsNone(self.f.to_python(""))
        self.assertIsNone(self.f.to_python(None))
        self.assertIsNone(self.f.to_python(" "))
        self.assertIsNone(self.f.prepare_value(None))
        self.assertEquals(timedelta(), self.f.to_python("a moment"))
        self.assertEquals(timedelta(), self.f.to_python(timedelta()))
        self.assertEquals(0, self.f.prepare_value(0))
        self.introspect(timedelta())
