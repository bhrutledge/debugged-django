from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User

from debugged.core.models import PublishedModel, PublishedManager
from debugged.attachments.models import AttachmentModel


class Post(PublishedModel, AttachmentModel):
    author = models.ForeignKey(User, related_name='posts')
    title = models.CharField(max_length=200)
    body = models.TextField()
    slug = models.SlugField(unique=True)

    objects = PublishedManager()
    
    class Meta:
        ordering = ['publish_date']
    
    def __unicode__(self):
        return self.title
        
    @models.permalink
    def get_absolute_url(self):
        return ('post_detail', [str(self.slug)])


from django.db.models.signals import pre_save
from debugged.core.signals import set_publish_date

pre_save.connect(set_publish_date, sender=Post)

