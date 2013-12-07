from django.conf import settings

RELEASE_TYPES = getattr(settings, "DEBUGGED_RELEASE_TYPES", 
                        [('download', 'Download'), ('ep', 'EP'), ('full-length', 'Full Length')])
