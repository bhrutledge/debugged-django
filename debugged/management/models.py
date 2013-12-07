from django.db import models

from debugged.calendar.models import Event

class EventReport(models.Model):
    event = models.ForeignKey(Event)
    door_income = models.PositiveIntegerField(blank=True, null=True)
    merch_income = models.PositiveIntegerField(blank=True, null=True)
    notes = models.TextField(blank=True)
    
    @property
    def parent(self):
        return self.event.parent
    
    @property
    def location(self):
        return "%s, %s, %s" % (self.event.location.name, self.event.location.city, self.event.location.region)
        
    class Meta:
        ordering = ['event__start_date']
    
    def __unicode__(self):
        return unicode(self.event)