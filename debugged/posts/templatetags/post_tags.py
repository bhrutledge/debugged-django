from django import template
from debugged.posts.models import Post

register = template.Library()

@register.inclusion_tag('posts/last_post.html')
def last_post():
    try:
        post = Post.objects.published().order_by('-publish_date')[0]
        return {'post': post}
    except IndexError:
        return None