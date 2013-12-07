from django.contrib import admin
from django.conf import settings

from debugged.calendar.models import Event
from debugged.attachments.admin import inlines as attachment_inlines

# TODO: Admin action for adding events to a parent


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['name', 'start_date', 'slug', 'object_type', 'location', 'poster', 'published', 'publish_date', 'featured']
        }),
        ('Details', {
            'classes': ['collapse closed'],
            'fields': ['parent', 'description', 'cost', 'ticket_url', 'start_time', 'end_date', 'end_time']
        }),
    ]
    
    raw_id_fields = ['location', 'parent']
    # TODO: http://code.djangoproject.com/ticket/9784
    # prepopulated_fields does not update on javascript (calendar) change
    prepopulated_fields = {'slug': ['start_date']}
    inlines = attachment_inlines
    list_display = ['start_date', 'name', 'object_type', 'location', 'parent', 'has_poster', 'published', 'featured']
    list_display_links = ['start_date', 'name']
    ordering = ['-start_date']
    list_editable = ['published', 'featured']
    list_filter = ['object_type', 'published', 'featured']
    date_hierarchy = 'start_date'
    search_fields = ['name', 'parent__name', 'location__name', 'location__city']
    
    class Media:
        css = {'all': ['calendar/css/inline.css', 'attachments/css/inline.css']}
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']


admin.site.register(Event, EventAdmin)

