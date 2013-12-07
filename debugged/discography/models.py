from datetime import date

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from debugged.core.models import PublishedModel, PublishedManager, PositionedModel
from debugged.contacts.models import Contact
from debugged.attachments.models import AttachmentModel
from debugged.discography.settings import RELEASE_TYPES

from filebrowser.fields import FileBrowseField


# TODO: Add description fields?

class Song(PublishedModel, AttachmentModel):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Contact, related_name='songs', blank=True, null=True)
    credits = models.TextField(blank=True)
    lyrics = models.TextField(blank=True)
    audio = FileBrowseField(max_length=200, format='Audio', directory="songs/", blank=True, null=True)
    artwork = FileBrowseField(max_length=200, format='Image', directory="artwork/", blank=True, null=True)
    slug = models.SlugField(unique=True)

    objects = PublishedManager()
    
    @property
    def parent(self):
        if self.tracks.count():
            return self.tracks.all()[0].parent
        return None
        
    def has_attachments(self):
        return (self.images.count() or self.videos.count() or 
                self.files.count() or self.links.count())
    has_attachments.short_description = "Attachments"
    has_attachments.boolean = True
        
    def has_details(self):
        return bool(self.lyrics) or bool(self.credits) or self.has_attachments()
    has_details.short_description = "Details"
    has_details.boolean = True
        
    def has_audio(self):
        return bool(self.audio)
    has_audio.short_description = "Audio"
    has_audio.boolean = True
        
    def has_artwork(self):
        return bool(self.artwork)
    has_artwork.short_description = "Artwork"
    has_artwork.boolean = True   

    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)

    @models.permalink
    def get_absolute_url(self):
        return ('song_detail', [str(self.slug)])
        

class Track(PositionedModel):
    song = models.ForeignKey(Song, related_name='tracks')
    
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey()
    number = models.PositiveIntegerField()
        
    class Meta:
        ordering = ['position']
        unique_together = ['content_type', 'object_id', 'number']

    # TODO: content_type is set incorrectly on an inline
    # def __unicode__(self):
    #     return u"%s (%s)" % (unicode(self.song), unicode(self.parent))
    
    def _get_position_filter(self):
        return models.Q(song=self.song)


class Release(PublishedModel, AttachmentModel):
    title = models.CharField(max_length=200)
    artist = models.ForeignKey(Contact, related_name='discography')
    object_type = models.CharField(max_length=200, choices=RELEASE_TYPES, verbose_name=_('type'))
    release_date = models.DateField(blank=True, null=True)
    label = models.ForeignKey(Contact, related_name='releases', blank=True, null=True)
    buy = models.TextField(blank=True)
    credits = models.TextField(blank=True)
    artwork = FileBrowseField(max_length=200, format='Image', directory="artwork/", blank=True, null=True)
    slug = models.SlugField(unique=True)    
    
    tracks = generic.GenericRelation(Track)
    
    objects = PublishedManager()
    
    def is_released(self):
        return self.release_date != None and self.release_date <= date.today()
    
    def has_attachments(self):
        return (self.images.count() or self.videos.count() or 
                self.files.count() or self.links.count())
    has_attachments.short_description = "Attachments"
    has_attachments.boolean = True

    def has_details(self):
        return bool(self.credits) or self.has_attachments()
    has_details.short_description = "Details"
    has_details.boolean = True
                
    def has_artwork(self):
        return bool(self.artwork)
    has_artwork.short_description = "Artwork"
    has_artwork.boolean = True
    
    class Meta:
        ordering = ['title']

    def __unicode__(self):
        return unicode(self.title)
        
    @models.permalink
    def get_absolute_url(self):
        return ('release_detail', [str(self.slug)])


from django.db.models.signals import pre_save
from debugged.core.signals import set_publish_date, set_position
        
pre_save.connect(set_publish_date, sender=Song)
pre_save.connect(set_publish_date, sender=Release)
pre_save.connect(set_position, sender=Track)
