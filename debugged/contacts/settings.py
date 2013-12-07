from django.conf import settings

CONTACT_TYPES = getattr(settings, "DEBUGGED_CONTACT_TYPES", [('person', 'Person'), ('org', 'Organization')])
LOCATION_TYPES = getattr(settings, "DEBUGGED_LOCATION_TYPES", [('bar', 'Bar'), ('restaurant', 'Restaurant')])
