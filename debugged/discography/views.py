from django.shortcuts import render_to_response
from django.template import RequestContext

from debugged.discography.models import Release, Song

def music_list(request):
    release_list = Release.objects.published().order_by('-release_date')
    song_list = Song.objects.published().filter(featured=True).exclude(audio='').order_by('-publish_date')
            
    return render_to_response('discography/music_list.html', 
                             {'release_list': release_list, 'song_list': song_list},
                              context_instance=RequestContext(request)) 
