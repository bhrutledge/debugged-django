from django import template

register = template.Library()
        
@register.inclusion_tag('contacts/contact_link.html')
def contactlink(contact):
    return {'contact': contact}
