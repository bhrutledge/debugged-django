from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

 
class StreamEntry(models.Model):
    # ContentType for all StreamItems
    item_type = models.ForeignKey(ContentType, related_name='streamentry_item_set')

    # Parent object for all StreamItems
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    parent = generic.GenericForeignKey()
    
    # TODO: Set description from model
    description = models.TextField(blank=True)
    publish_date = models.DateTimeField()
    modify_date = models.DateTimeField()
                                    
    def item_count(self):
        return self.items.count()

    def item_title(self):
        title = self.items.all()[0].content.title
        if self.items.count() > 1:
            title = title + ", ..."
        return title
        
    class Meta(object):
        verbose_name_plural = "stream entries"

    def __unicode__(self):
        return "%s, %s, %s" % (unicode(self.publish_date),
                               unicode(self.item_type).capitalize(), 
                               self.item_title())

class StreamItem(models.Model):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content = generic.GenericForeignKey()
    
    # TODO: Add featured field and manager
    publish_date = models.DateTimeField()
    modify_date = models.DateTimeField()

    entry = models.ForeignKey(StreamEntry, related_name='items')


    def __unicode__(self):
        return unicode(self.content)
