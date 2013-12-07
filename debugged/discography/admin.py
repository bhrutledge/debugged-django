from django.contrib import admin
from django.conf import settings

from debugged.discography.models import Song, Track, Release
from debugged.attachments.admin import inlines as attachment_inlines


class TrackInline(admin.TabularInline):
    model = Track
    fields = ['position', 'content_type', 'object_id', 'number']
    extra = 1
    classes = ['collapse closed']
    allow_add = True


class ReleaseAdmin(admin.ModelAdmin):    
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'artist', 'object_type', 'artwork', 'published', 'publish_date', 'featured']
        }),
        ('Details', {
            'classes': ['collapse closed'],
            'fields': ['release_date', 'label', 'credits', 'buy']
        }),
    ]
    
    raw_id_fields = ['artist', 'label']
    prepopulated_fields = {'slug': ['title']}
    inlines = attachment_inlines
    list_display = ['title', 'artist', 'object_type', 'release_date', 'label', 'has_artwork', 'published', 'featured']
    list_editable = ['published', 'featured']
    list_filter = ['object_type', 'published', 'featured']
    date_hierarchy = 'release_date'
    search_fields = ['title']
    
    class Media:
        css = {'all': ['attachments/css/inline.css']}
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']


class SongAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['title', 'slug', 'artist', 'audio', 'artwork', 'published', 'publish_date', 'featured']
        }),
        ('Details', {
            'classes': ['collapse closed'],
            'fields': ['credits', 'lyrics']
        }),
    ]
    
    raw_id_fields = ['artist']
    prepopulated_fields = {'slug': ['title']}
    inlines = [TrackInline] + attachment_inlines
    ordering = ['title']
    list_display = ['title', 'artist', 'parent', 'has_audio', 'has_artwork', 'published', 'featured']
    list_editable = ['published', 'featured']
    list_filter = ['published', 'featured']
    search_fields = ['title']
    
    class Media:
        css = {'all': ['discography/css/inline.css', 'attachments/css/inline.css']}
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']
        

class TrackAdmin(admin.ModelAdmin):
    fields =  ['song', 'content_type', 'object_id', 'number', 'position']
    ordering = ['song']
    list_display = ['song', 'parent', 'number']


admin.site.register(Release, ReleaseAdmin)
admin.site.register(Song, SongAdmin)
#admin.site.register(Track, TrackAdmin)
