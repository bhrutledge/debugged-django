from django.conf import settings

STREAM_ITEMS = getattr(settings, "DEBUGGED_STREAM_ITEMS", [])