from debugged.bandsite.forms import ContactForm, MailingListForm

def forms(request):
    return {'email_form': ContactForm(auto_id='email_%s'),
            'list_form': MailingListForm(auto_id='list_%s')}
