from time import strftime
from django import template
from debugged.core.templatetags import parse_string, parse_args, get_num
from debugged.calendar.models import Event

register = template.Library()

class ShowEventsNode(template.Node):
    def __init__(self, events_var, format):
        self.events_var = template.Variable(events_var)
        self.format = format

    def render(self, context):
        event_list = self.events_var.resolve(context)
        if not event_list:
            return ''

        context['event_list'] = event_list

        t = template.loader.get_template('calendar/event_list_%s.html' % self.format)
        return t.render(context)


class UpcomingEventsNode(template.Node):
    def __init__(self, num=None):
        self.num = num

    def render(self, context):
        qs = Event.objects.upcoming().filter(featured=True)
        if qs.count() == 0:
            qs = Event.objects.upcoming()
            
        if qs.count() and self.num:
            context['more_events'] = qs.count() - self.num
            qs = qs[:self.num]

        context['event_list'] = qs

        t = template.loader.get_template('calendar/upcoming_events.html')
        return t.render(context)
        

@register.tag
def events(parser, token):
    """
    events from <events_var> format "<format>"
    """

    bits = token.split_contents()
    bits.reverse()

    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['from', 'format'])
    events_var = tag_args.get('from')
    format = tag_args.get('format')
    
    if not events_var:
        raise template.TemplateSyntaxError, "%r is missing 'from' parameter" % tag_name
        
    if format:
        format = parse_string(tag_name, format, 'event format')
    else:
        raise template.TemplateSyntaxError, "%r is missing 'format' parameter" % tag_name
    
    return ShowEventsNode(events_var, format)
    
@register.tag
def upcoming_events(parser, token):
    """
    upcoming_events [limit <num>]
    """

    bits = token.split_contents()
    bits.reverse()    

    tag_name = bits.pop()
    tag_args = parse_args(tag_name, bits, ['limit'])

    num = get_num(tag_name, tag_args)

    return UpcomingEventsNode(num)

@register.inclusion_tag('calendar/event_years.html')
def event_years(current_year=None):
    year_func = lambda x: strftime('%Y', x.timetuple()) 
    archive_years = Event.objects.past().dates('start_date', 'year', order='DESC')
    return {'archive_years': map(year_func, archive_years),
            'current_year': current_year}

