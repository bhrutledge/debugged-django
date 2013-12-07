from datetime import datetime

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic

from debugged.core.utils import format_dates
from debugged.core.models import PublishedModel, PublishedManager, PositionedModel
from debugged.contacts.models import Location, Contact
from debugged.attachments.models import AttachmentModel
from debugged.discography.models import Track
from debugged.calendar.settings import EVENT_TYPES

from filebrowser.fields import FileBrowseField


class EventManager(PublishedManager):
    def upcoming(self):
        return self.published().filter(end_date__gte=datetime.now())
        
    def past(self):
        return self.published().exclude(end_date__gte=datetime.now())


class Event(PublishedModel, AttachmentModel):
    name = models.CharField(max_length=200, blank=True)
    object_type = models.CharField(max_length=200, choices=EVENT_TYPES, verbose_name=_('type'))
    location = models.ForeignKey(Location, related_name='events', blank=True, null=True)
    parent = models.ForeignKey('self', related_name='children', blank=True, null=True)
    description = models.TextField(blank=True)
    cost = models.CharField(max_length=200, blank=True)
    ticket_url = models.URLField(verify_exists=False, blank=True, verbose_name=_('ticket URL'))
    poster = FileBrowseField(max_length=200, format='Image', directory="posters/", blank=True, null=True)
    slug = models.SlugField(unique=True)
    
    # TODO: Add map_url
        
    start_date = models.DateField()
    start_time = models.TimeField(blank=True, null=True)
    end_date = models.DateField(blank=True)
    end_time = models.TimeField(blank=True, null=True)
    
    tracks = generic.GenericRelation(Track)
        
    objects = EventManager()    

    @property
    def dates(self):
        return format_dates(self.start_date, self.end_date)
        
    @property
    def title(self):
        title = self.dates
        if self.name:
            title = self.name
        
        if self.location:
            title = title + u" in %s, %s" % (self.location.city, self.location.region)

        return title

    def is_upcoming(self):
        return self.end_date >= datetime.now().date()
    is_upcoming.short_description = "Upcoming"
    is_upcoming.boolean = True

    def has_attachments(self):
        return (self.images.count() or self.videos.count() or 
                self.files.count() or self.links.count())
    has_attachments.short_description = "Attachments"
    has_attachments.boolean = True

    def has_details(self):
        return self.has_attachments()
    has_details.short_description = "Details"
    has_details.boolean = True
    
    def has_poster(self):
        return bool(self.poster)
    has_poster.short_description = "Poster"
    has_poster.boolean = True
     
    class Meta:
        ordering = ['start_date', 'start_time', 'parent__id']
        
    def __unicode__(self):
        return self.title
            
    @models.permalink
    def get_absolute_url(self):
        return ('calendar_detail', [str(self.slug)])
            
    def save(self, force_insert=False, force_update=False):
        if not self.end_date or self.start_date > self.end_date:
            self.end_date = self.start_date

        # TODO: Set start/end times
        super(Event, self).save(force_insert, force_update)
        
        if self.parent:
            if self.parent.start_date > self.start_date:
                self.parent.start_date = self.start_date
            if self.parent.end_date < self.end_date:
                self.parent.end_date = self.end_date
                
            self.parent.save()


from django.db.models.signals import pre_save
from debugged.core.signals import set_publish_date, set_position

pre_save.connect(set_publish_date, sender=Event)
