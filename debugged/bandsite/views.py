from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.contenttypes.models import ContentType

from debugged.attachments.models import Link
from debugged.discography.models import Release
from debugged.calendar.models import Event
from debugged.bandsite.forms import MailingListForm, ContactForm
from debugged.bandsite.utils import process_contact, process_mailing_list


def contact_form(request):
    auto_id = 'contact_%s'

    if request.method == 'POST':
        form = ContactForm(request.POST, auto_id=auto_id)
        if form.is_valid():
            process_contact(form)            
    else:
        form = ContactForm(auto_id=auto_id)

    return render_to_response('bandsite/contact_form.html',
                              {'contact_form': form},
                              context_instance=RequestContext(request))
                              
def mailing_list_form(request):
    auto_id = 'mailing_list_%s'

    if request.method == 'POST':
        form = MailingListForm(request.POST, auto_id=auto_id)
        if form.is_valid():
            process_mailing_list(form)            
    else:
        form = MailingListForm(auto_id=auto_id)

    return render_to_response('bandsite/mailing_list_form.html',
                              {'mailing_list_form': form},
                              context_instance=RequestContext(request))

def press_list(request):
    release_press = []
    for release in Release.objects.published().order_by('-release_date'):
        links = release.links.published().filter(object_type='press').order_by('-featured', '-source_date')
            
        if links.count():
            release_press.append({'release': release, 'press': links})
            
    event_type = ContentType.objects.get_for_model(Event)
    event_press = Link.objects.published().filter(content_type=event_type, object_type='press').order_by('-featured', '-source_date')
        
    return render_to_response('bandsite/press_list.html', 
                             {'release_press': release_press, 'event_press': event_press},
                             context_instance=RequestContext(request)) 
