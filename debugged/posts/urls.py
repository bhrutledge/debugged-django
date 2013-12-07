from django.conf.urls.defaults import *
from debugged.posts.models import Post
    
posts = {
    'queryset': Post.objects.published(),
    'template_object_name': 'post',
}

pages = {
    'queryset': Post.objects.published().reverse(),
    'template_object_name': 'post',
    # TODO: Use a year archive instead?
    'paginate_by': 5,
}

urlpatterns = patterns('django.views.generic',
    url(r'^$', 'list_detail.object_list', pages, name='posts'),
    url(r'^(?P<slug>[-\w]+)/$', 'list_detail.object_detail', posts, name='post_detail'),
)
