from django import template

register = template.Library()

class StreamItemNode(template.Node):
    def __init__(self, entry_var):
        self.entry_var = template.Variable(entry_var)

    def render(self, context):
        entry = self.entry_var.resolve(context)
        template_name = 'stream/%s.html' % (entry.item_type.model)
        context['entry'] = entry
        
        return template.loader.get_template(template_name).render(context)

@register.tag
def streamentry(parser, token):
    """
    streamentry <entry_var>
    """

    bits = token.split_contents()
    bits.reverse()
    tag_name = bits.pop()
    
    try:
        entry_var = bits.pop()
    except IndexError:
        raise template.TemplateSyntaxError, "%r is missing entry argument" % tag_name
        
    if bits:
        raise template.TemplateSyntaxError, "%r has unexpected arguments" % tag_name

    return StreamItemNode(entry_var)
