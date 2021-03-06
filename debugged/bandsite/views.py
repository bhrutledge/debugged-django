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
    all_press = Link.objects.published().filter(object_type='press').order_by('-source_date')

    return render_to_response('bandsite/press_list.html',
                              { 'all_press': all_press, },
                              context_instance=RequestContext(request))
