from django.conf.urls.defaults import *
from debugged.discography.models import Release, Song

songs = {
    'queryset': Song.objects.published(),
    'template_object_name': 'song',
}

releases = {
    'queryset': Release.objects.published().order_by('-release_date'),
    'template_object_name': 'release',
}

lyrics = {
    'queryset': Release.objects.published(),
    'template_object_name': 'release',
    'template_name': 'discography/release_lyrics.html',
}

urlpatterns = patterns('',
    url(r'^$', 'debugged.discography.views.music_list', name='music'),
    url(r'^songs/$', 'django.views.generic.list_detail.object_list', songs, name='songs'),
    url(r'^songs/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', songs, name='song_detail'),
    url(r'^releases/$', 'django.views.generic.list_detail.object_list', releases, name='releases'),
    url(r'^releases/(?P<slug>[-\w]+)/$', 'django.views.generic.list_detail.object_detail', releases, name='release_detail'),
    url(r'^releases/(?P<slug>[-\w]+)/lyrics$', 'django.views.generic.list_detail.object_detail', lyrics, name='release_lyrics'),
)
