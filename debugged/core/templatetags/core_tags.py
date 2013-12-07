import re
from django import template
from django.utils.html import escape, conditional_escape
from django.utils.safestring import mark_safe
from django.contrib.sites.models import Site

register = template.Library()
    
@register.simple_tag
def daterange(start_date, end_date):
    from debugged.core.utils import format_dates
    return format_dates(start_date, end_date)

@register.inclusion_tag('core/page_nav.html')
def pagenav(paginator, page_obj):
    return {'paginator': paginator, 'page_obj': page_obj, 'first_page': 1}
            
@register.filter()
def obfuscate(email, linktext=None, autoescape=None):
    """
    Given a string representing an email address,
	returns a mailto link with rot13 JavaScript obfuscation.

    Accepts an optional argument to use as the link text;
	otherwise uses the email address itself.
    """
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x

    email = re.sub('@','\\\\100', re.sub('\.', '\\\\056', esc(email))).encode('rot13')

    if linktext:
        linktext = esc(linktext).encode('rot13')
    else:
        linktext = email

    rotten_link = """<script type="text/javascript">/*<![CDATA[*/document.write \
        ("<n uers=\\\"znvygb:%s\\\">%s<\\057n>".replace(/[a-zA-Z]/g, \
        function(c){return String.fromCharCode((c<="Z"?90:122)>=\
        (c=c.charCodeAt(0)+13)?c:c-26);}));/*]]>*/</script>""" % (email, linktext)
    return mark_safe(rotten_link)
obfuscate.needs_autoescape = True  

@register.simple_tag
def emaillink(subject, email):
    current_site = Site.objects.get_current()
    mailto = "%s?subject=%s %s" % (email, current_site.name, subject)
    return obfuscate(mailto, email, autoescape=True)
