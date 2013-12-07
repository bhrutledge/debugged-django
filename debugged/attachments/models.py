import re

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

from debugged.core.models import PublishedModel, PublishedManager, PositionedModel
from debugged.contacts.models import Contact
from debugged.attachments.settings import *
        
from filebrowser.fields import FileBrowseField


class Attachment(PublishedModel, PositionedModel):            
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    parent = generic.GenericForeignKey()

    objects = PublishedManager()

    class Meta:
        abstract = True
        app_label = 'attachments'
        ordering = ['position']

    def __unicode__(self):
        return unicode(self.title)
        
    # TODO: Don't set position for attachments w/o parent?
    def _get_position_filter(self):
        return models.Q(content_type=self.content_type) & models.Q(object_id=self.object_id)
         
    def save(self, force_insert=False, force_update=False):
        if not self.content_type:
            self.object_id = self.position = None
        
        super(Attachment, self).save(force_insert, force_update)


# TODO: Add alt text
# TODO: Replace creator with credit CharField
class Image(Attachment):
    object_type = models.CharField(max_length=200, choices=IMAGE_TYPES, verbose_name=_('type'))
    image = FileBrowseField(max_length=200, format='Image', directory="images/")
    creator = models.ForeignKey(Contact, related_name='images', blank=True, null=True)


class File(Attachment):
    object_type = models.CharField(max_length=200, choices=FILE_TYPES, verbose_name=_('type'))
    file = FileBrowseField(max_length=200)


class Link(Attachment):
    object_type = models.CharField(max_length=200, choices=LINK_TYPES, verbose_name=_('type'))
    url = models.URLField(verify_exists=False, verbose_name=_('URL'))
    source_date = models.DateField(blank=True, null=True, verbose_name=_('date'))
    quote = models.BooleanField(default=False)
    

class Video(Attachment):
    object_type = models.CharField(max_length=200, choices=VIDEO_TYPES, verbose_name=_('type'))
    url = models.URLField(verify_exists=False)
    source = models.CharField(max_length=200, blank=True, null=True)
    clip = models.CharField(max_length=200, blank=True, null=True)
    creator = models.ForeignKey(Contact, related_name='video', blank=True, null=True)
    
    def save(self, force_insert=False, force_update=False):
        for source in VIDEO_SOURCES:
            match = re.search(source[0], self.url)
            if match:
                self.source = source[1]
                self.clip = match.group(1)
                break
        
        super(Video, self).save(force_insert, force_update)


class AttachmentModel(models.Model):
    images = generic.GenericRelation(Image)
    files = generic.GenericRelation(File)
    videos = generic.GenericRelation(Video)
    links = generic.GenericRelation(Link)

    class Meta:
        abstract = True
        

from django.db.models.signals import pre_save
from debugged.core.signals import set_publish_date, set_position

for model in [Image, File, Link, Video]:
    pre_save.connect(set_publish_date, sender=model)
    pre_save.connect(set_position, sender=model)

