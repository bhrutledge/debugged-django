from django import template
from debugged.bandsite.settings import *

register = template.Library()

@register.inclusion_tag('bandsite/contact_emails.html')
def contact_emails(current_year=None):
    return {'contact_emails': CONTACT_EMAILS}
