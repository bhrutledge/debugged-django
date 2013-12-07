from django.conf import settings

CONTACT_EMAILS = getattr(settings, "BANDSITE_CONTACT_EMAILS", [('General', '"John Doe" <john@doe.com>')])
LIST_EMAIL = getattr(settings, "BANDSITE_LIST_EMAIL", None)