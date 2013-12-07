from django.conf import settings

EVENT_TYPES = getattr(settings, "DEBUGGED_EVENT_TYPES", [('gig', 'Gig'), ('tour', 'Tour')])
