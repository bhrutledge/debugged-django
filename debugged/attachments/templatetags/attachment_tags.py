from django import template
from debugged.core.templatetags import *

register = template.Library()

def get_attachment_set(context, att_list_var, att_types=[], exclude=False, num=None):
    # TODO: Handle missing variables more cleanly
    att_list = att_list_var.resolve(context)
    qs = att_list.all()
    if att_types:
        if exclude:
            qs = qs.exclude(object_type__in=att_types)
        else:
            qs = qs.filter(object_type__in=att_types)

    if qs.count() and num:
        qs = qs[:num]
        
    return qs

def get_template(query_set, suffix=''):
    model_type = query_set.model.__name__.lower()
    return template.loader.get_template('attachments/%s%s.html' % (model_type, suffix))

# TODO: Add show_attachment

class ShowFirstAttachmentNode(template.Node):
    def __init__(self, att_list_var, att_types=[], exclude=False):
        self.att_list_var = template.Variable(att_list_var)
        self.att_types = att_types
        self.exclude = exclude

    def render(self, context):
        qs = get_attachment_set(context, self.att_list_var, self.att_types, self.exclude)
        if qs.count() == 0:
            return ''
          
        # TODO: Research re-using context vs. new Context/RequestContext     
        context['attachment'] = qs[0]        
        return get_template(qs).render(context)


class ShowAttachmentsNode(template.Node):
    def __init__(self, att_list_var, att_types=[], exclude=False, num=None):
        self.att_list_var = template.Variable(att_list_var)
        self.att_types = att_types
        self.exclude = exclude
        self.num = num

    def render(self, context):
        qs = get_attachment_set(context, self.att_list_var, self.att_types, self.exclude, self.num)
        if qs.count() == 0:
            return ''
                  
        context['attachments'] = qs
        return get_template(qs, '_list').render(context)

      
class GetFirstAttachmentNode(template.Node):
    def __init__(self, att_list_var, context_var, att_types=[], exclude=False):
        self.att_list_var = template.Variable(att_list_var)
        self.context_var = context_var
        self.att_types = att_types
        self.exclude = exclude

    def render(self, context):
        context[self.context_var] = None

        qs = get_attachment_set(context, self.att_list_var, self.att_types, self.exclude)
        if qs.count():        
            context[self.context_var] = qs[0]

        return ''


class GetAttachmentsNode(template.Node):
    def __init__(self, att_list_var, context_var, att_types=[], exclude=False, num=None):
        self.att_list_var = template.Variable(att_list_var)
        self.context_var = context_var
        self.att_types = att_types
        self.exclude = exclude
        self.num = num
    
    def render(self, context):
        context[self.context_var] = None

        qs = get_attachment_set(context, self.att_list_var, self.att_types, self.exclude, self.num)
        if qs.count():        
            context[self.context_var] = qs
        
        return ''

@register.tag
def first_attachment(parser, token):
    """
    first_attachment from <att_list_var> [only|not "<att_type>[,<att_type>...]"] [as <context_var>]
    """

    bits = token.split_contents()
    bits.reverse()    

    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['from', 'as', 'only', 'not'])

    att_list_var = get_att_list_var(tag_name, tag_args)
    context_var = get_context_var(tag_name, tag_args)
    att_types, exclude = get_att_types(tag_name, tag_args)

    if context_var:
        return GetFirstAttachmentNode(att_list_var, context_var, att_types, exclude)
        
    return ShowFirstAttachmentNode(att_list_var, att_types, exclude)

@register.tag
def attachments(parser, token):
    """
    attachments from <att_list_var> [only|not "<att_type>[,<att_type>...]"] [limit <num>] [as <context_var>]
    """
    
    bits = token.split_contents()
    bits.reverse()    
    
    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['from', 'as', 'only', 'not', 'limit'])
 
    att_list_var = get_att_list_var(tag_name, tag_args)
    context_var = get_context_var(tag_name, tag_args)
    att_types, exclude = get_att_types(tag_name, tag_args)
    num = get_num(tag_name, tag_args)

    if context_var:
        return GetAttachmentsNode(att_list_var, context_var, att_types, exclude, num)
        
    return ShowAttachmentsNode(att_list_var, att_types, exclude, num)
