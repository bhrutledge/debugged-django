from django.core.mail import send_mail
from django.conf import settings
from debugged.bandsite.settings import *
    

def process_contact(form):
    subject = form.cleaned_data['subject']
    sender = '"%s" <%s>' % (form.cleaned_data['sender_name'], form.cleaned_data['sender_email'])
    message = form.cleaned_data['message']
    
    recipient = None
    for contact in CONTACT_EMAILS:
        if subject == contact['subject']:
            recipient = contact['email']
            break
    
    if recipient:
        subject = settings.EMAIL_SUBJECT_PREFIX + subject
        send_mail(subject, message, sender, [recipient], fail_silently=False)
        
        admin = settings.ADMINS[0][1]
        send_mail(subject, message, sender, [admin], fail_silently=False)
        
def process_mailing_list(form):
    sender = form.cleaned_data['sender_email']
    send_mail("subscribe", "subscribe", sender, [LIST_EMAIL], fail_silently=False)
