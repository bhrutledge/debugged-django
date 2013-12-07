from django import template
from debugged.discography.models import *
from debugged.core.templatetags import *

register = template.Library()

class FeaturedDiscographyNode(template.Node):
    def __init__(self, disc_model, slug=None, artwork=None):
        self.disc_model = disc_model
        self.slug = slug
        self.artwork = artwork

    def render(self, context):
        disc_obj = None

        try:
            if self.slug:
                disc_obj = self.disc_model.objects.get(slug=self.slug)
            else:
                disc_obj = self.disc_model.objects.featured().order_by('-feature_date')[0]
        except self.disc_model.DoesNotExist, IndexError:
            return ''
            
        model_type = self.disc_model.__name__.lower()
        context[model_type] = disc_obj
        context['artwork'] = self.artwork
        template_name = 'discography/featured_%s.html' % model_type

        return template.loader.get_template(template_name).render(context)


def featured_discography(disc_model, parser, token):
    bits = token.split_contents()
    bits.reverse()    

    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['slug', 'artwork'])

    slug = tag_args.get('slug')
    if slug:
        slug = parse_string(tag_name, slug, 'slug')
    
    artwork = tag_args.get('artwork')
    if artwork:
        artwork = parse_string(tag_name, artwork, 'artwork')

    return FeaturedDiscographyNode(disc_model, slug, artwork) 

@register.tag
def featured_release(parser, token):
    """
    featured_release [slug "<slug>"] [artwork "thumbnail|medium|..."]
    """
    return featured_discography(Release, parser, token)
    
@register.tag
def featured_song(parser, token):
    """
    featured_song [slug "<slug>"] [artwork "thumbnail|medium|..."]
    """
    return featured_discography(Song, parser, token)
