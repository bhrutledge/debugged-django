from django.db import models
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType

class Parent(models.Model):
    name = models.CharField(max_length=200)
    
class Attachment(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(Parent)
    slug = models.SlugField()
    
    class Meta:
        unique_together = ['parent', 'slug']
    
class GenericAttachment(models.Model):
    name = models.CharField(max_length=200)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    parent = generic.GenericForeignKey()
    slug = models.SlugField()
    
    class Meta:
        unique_together = ['content_type', 'object_id', 'slug']
