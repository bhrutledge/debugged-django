from django import forms
from django.utils.translation import ugettext as _

from debugged.bandsite.settings import *

class MailingListForm(forms.Form):
    sender_email = forms.EmailField(label=_('Your email'))
    
class ContactForm(forms.Form):
    def _contact_choices():
        choices = []
        for contact in CONTACT_EMAILS:
            choices.append((contact['subject'], contact['subject']))
        return choices
    
    subject = forms.ChoiceField(choices=_contact_choices())
    sender_name = forms.CharField(max_length=100, label=_('Your name'))
    sender_email = forms.EmailField(label=_('Your email'))
    message = forms.CharField(widget=forms.Textarea)
    