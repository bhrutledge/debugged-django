from django.contrib import admin

from debugged.management.models import EventReport

class EventReportAdmin(admin.ModelAdmin):    
    raw_id_fields = ['event']
    list_display = ['event', 'location', 'parent', 'door_income', 'merch_income']
    search_fields = ['event__location__name', 'event__location__city', 'event__parent__name']

admin.site.register(EventReport, EventReportAdmin)
