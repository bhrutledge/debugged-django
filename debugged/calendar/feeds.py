from django.core.urlresolvers import reverse
from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

from debugged.calendar.models import Event

class CalendarFeed(Feed):
    
    def title(self, obj):
        return Site.objects.get_current().name + " Calendar";
        
    def description(self, obj):
        return self.title(obj)
    
    def link(self, obj):
        return reverse('calendar')

    def items(self):
        return Event.objects.published().order_by('-publish_date')[:10]
        
    def item_pubdate(self, item):
        return item.publish_date
