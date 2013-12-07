from datetime import datetime
from django.db.models import Q
from django.conf.urls.defaults import *
from debugged.calendar.models import Event
    
upcoming = {
    'queryset': Event.objects.upcoming(),
    'template_object_name': 'event',
}

archive = {
    'queryset': Event.objects.published(),
    'date_field': 'end_date',
    'make_object_list': True,
    'template_object_name': 'event',
}

events = {
    'queryset': Event.objects.published(),
    'template_object_name': 'event',
}

# TODO: Move paginate_by to setting
posters = {
    'queryset': Event.objects.published().exclude(Q(poster__isnull=True) | Q(poster__exact='')).reverse(),
    'template_object_name': 'event',
    'template_name': 'calendar/poster_list.html',
    'paginate_by': 12,
}

# TODO: Add an archive index view?
# TODO: Add a year argument to basic list view?
urlpatterns = patterns('django.views.generic',
    url(r'^$', 'list_detail.object_list', upcoming, name='calendar'),
    url(r'^posters/$', 'list_detail.object_list', posters, name='posters'),
    url(r'^(?P<year>\d{4})/$', 'date_based.archive_year',  archive, name='calendar_archive'),
    url(r'^(?P<slug>[-\w]+)/$', 'list_detail.object_detail', events, name='calendar_detail'),
)
