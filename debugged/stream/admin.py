from django.contrib import admin
from django.conf import settings

from debugged.stream.models import StreamEntry

class StreamEntryAdmin(admin.ModelAdmin):
    fields = ['description']
    list_display = ['publish_date', 'item_type', 'item_count', 'item_title', 'parent']
    ordering = ['-publish_date']
    date_hierarchy = 'publish_date'
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']

admin.site.register(StreamEntry, StreamEntryAdmin)
