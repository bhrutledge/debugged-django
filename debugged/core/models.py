from django.db import models

# TODO: http://www.djangosnippets.org/snippets/734/
class QuerySetManager(models.Manager):
    use_for_related_fields = True

    def __init__(self, qs_class=models.query.QuerySet):
        super(QuerySetManager, self).__init__()
        self.qs_class = qs_class
    
    def get_query_set(self):
        return self.qs_class(self.model)
    
    def __getattr__(self, attr):
        return super(QuerySetManager, self).__getattr__(attr)


class PublishedManager(models.Manager):
    use_for_related_fields = True

    def published(self):
        return self.filter(published=True)

    def featured(self):
        return self.published().filter(featured=True)


class PublishedModel(models.Model):
    # TODO: Rename publish_date and modify_date
    published = models.BooleanField(default=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    modify_date = models.DateTimeField(editable=False, blank=True, null=True)
    featured = models.BooleanField(default=False)
    feature_date = models.DateTimeField(editable=False, blank=True, null=True)
    
    class Meta:
        abstract = True
        
class PositionedModel(models.Model):
    position = models.PositiveIntegerField(blank=True)
    
    class Meta:
        abstract = True
        
    def _get_position_filter(self):
        return models.Q()
