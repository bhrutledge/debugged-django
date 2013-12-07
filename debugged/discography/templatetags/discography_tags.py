from django import template
from debugged.discography.models import Release, Song

register = template.Library()

@register.inclusion_tag('discography/release_link.html')
def releaselink(release):
    if type(release) != Release:
        try:
            release = Release.objects.get(slug=release)
        except Release.DoesNotExist:
            return None

    return {'release': release}
        
@register.inclusion_tag('discography/song_link.html')
def songlink(song):
    if type(song) != Song:
        try:
            song = Song.objects.get(slug=song)
        except Song.DoesNotExist:
            return None

    return {'song': song}
