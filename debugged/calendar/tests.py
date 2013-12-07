import os
import unittest
import datetime

from debugged.calendar.models import Event, Flyer

class EventUnicodeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.start_date = datetime.date.today()
        self.end_date = self.start_date + datetime.timedelta(days=1)
        self.name = u"Foo"
        
        self.event = Event()
        self.event.start_date = self.start_date
        self.event.save()
        
    def testOnlyStart(self):
        self.assertEqual(unicode(self.event), unicode(self.start_date))
    
    def testStartAndEnd(self):
        self.event.end_date = self.end_date
        self.assertEqual(unicode(self.event), 
                         u"%s - %s" % (self.start_date, self.end_date))
                         
    def testName(self):
        self.event.name = self.name
        self.assertEqual(unicode(self.event), self.name)

    def tearDown(self):
        Event.objects.all().delete()