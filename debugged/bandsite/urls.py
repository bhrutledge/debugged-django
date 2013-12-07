from django.conf.urls.defaults import *
from debugged.attachments.models import Image, Video

# TODO: Move paginate_by to setting

video = {
    'queryset': Video.objects.published().order_by('-publish_date'),
    'template_object_name': 'video',
    'template_name': 'bandsite/video_list.html',
    'paginate_by': 4,
}

photos = {
    'queryset': Image.objects.featured().order_by('-feature_date'),
    'template_object_name': 'photo',
    'template_name': 'bandsite/photo_list.html',
    'paginate_by': 12,
}

urlpatterns = patterns('',
    url(r'^photos/$', 'django.views.generic.list_detail.object_list', photos, name='photos'),
    url(r'^video/$', 'django.views.generic.list_detail.object_list', video, name='video'),
    url(r'^press/$', 'debugged.bandsite.views.press_list', name='press'),
    url(r'^contact/$', 'debugged.bandsite.views.contact_form', name='contact'),
    url(r'^mailing-list/$', 'debugged.bandsite.views.mailing_list_form', name='mailing_list')
)
