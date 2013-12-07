from django import template
from debugged.attachments.models import *
from debugged.core.templatetags import *

register = template.Library()

class FeaturedAttachmentsNode(template.Node):
    def __init__(self, att_model, att_types=[], exclude=False, num=None):
        self.att_model = att_model
        self.att_types = att_types
        self.exclude = exclude
        self.num = num

    def render(self, context):
        qs = self.att_model.objects.featured().order_by('-feature_date')
        
        if self.att_types:
            if self.exclude:
                qs = qs.exclude(object_type__in=self.att_types)
            else:
                qs = qs.filter(object_type__in=self.att_types)
        
        if qs.count() and self.num:
            qs = qs[:self.num]
            
        model_type = self.att_model.__name__.lower()
        context[model_type + '_list'] = qs
        template_name = 'attachments/featured_%s_list.html' % model_type

        return template.loader.get_template(template_name).render(context)


def featured_attachments(att_model, parser, token):
    bits = token.split_contents()
    bits.reverse()    

    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['only', 'not', 'limit'])

    att_types, exclude = get_att_types(tag_name, tag_args)
    num = get_num(tag_name, tag_args)

    return FeaturedAttachmentsNode(att_model, att_types, exclude, num) 

@register.tag
def featured_files(parser, token):
    """
    featured_files [only|not "<att_type>[,<att_type>...]"] [limit <num>]
    """
    return featured_attachments(File, parser, token)

@register.tag
def featured_images(parser, token):
    """
    featured_images [only|not "<att_type>[,<att_type>...]"] [limit <num>]
    """
    return featured_attachments(Image, parser, token)

@register.tag
def featured_links(parser, token):
    """
    featured_links [only|not "<att_type>[,<att_type>...]"] [limit <num>]
    """
    return featured_attachments(Link, parser, token)

@register.tag
def featured_videos(parser, token):
    """
    featured_videos [only|not "<att_type>[,<att_type>...]"] [limit <num>]
    """
    return featured_attachments(Video, parser, token)
