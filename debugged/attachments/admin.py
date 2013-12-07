from django.conf import settings
from django.contrib import admin
from django.contrib.contenttypes import generic

from filebrowser.settings import ADMIN_THUMBNAIL
from debugged.attachments.models import Image, File, Link, Video


class AttachmentInline(generic.GenericStackedInline):
    extra = 0
    classes = ['collapse closed']
    sortable_field_name = "position"
    allow_add = True


class ImageInline(AttachmentInline):
    model = Image
    fields = ['position', 'object_type', 'title', 'image', 'published', 'featured']


class FileInline(AttachmentInline):
    model = File
    fields = ['position', 'object_type', 'title', 'file', 'published', 'featured']
    

class LinkInline(AttachmentInline):
    model = Link
    fields = ['position', 'object_type', 'title', 'url', 'published', 'featured']


class VideoInline(AttachmentInline):
    model = Video
    fields = ['position', 'object_type', 'title', 'url', 'published', 'featured']


inlines = [ImageInline, FileInline, LinkInline, VideoInline]

# TODO: Research sitewide admin media class
class AttachmentAdmin(admin.ModelAdmin):
    save_as = True
    save_on_top = True
    ordering = ['title']
    list_editable = ['published', 'featured']
    list_filter = ['object_type', 'published', 'featured']
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']


class ImageAdmin(AttachmentAdmin):
    def thumbnail(self, instance):
        if instance.image:
            return '<img src="%s" />' % instance.image.version_generate(ADMIN_THUMBNAIL).url
        else:
            return ""
    thumbnail.allow_tags = True
    
    fieldsets = [
        (None, {
            'fields': ['object_type', 'title', 'image', 'creator', 'description', 'published', 'publish_date', 'featured']
        }),
        ('Parent', {
            'fields': ['content_type', 'object_id', 'position']
        })
    ]
    # TODO: Link to parent change page
    raw_id_fields = ['creator']
    list_display = ['thumbnail', 'title', 'object_type', 'parent', 'published', 'featured']
    list_display_links = ['title']


class FileAdmin(AttachmentAdmin):
    fieldsets = [
        (None, {
            'fields': ['object_type', 'title', 'file', 'description', 'published', 'publish_date', 'featured']
        }),
        ('Parent', {
            'fields': ['content_type', 'object_id', 'position']
        })
    ]
    list_display = ['title', 'object_type', 'file', 'parent', 'published', 'featured']
    

class LinkAdmin(AttachmentAdmin):
    fieldsets = [
        (None, {
            'fields': ['object_type', 'title', 'source_date', 'url', 'description', 'quote', 'published', 'publish_date', 'featured']
        }),
        ('Parent', {
            'fields': ['content_type', 'object_id', 'position']
        })
    ]
    list_display = ['title', 'object_type', 'source_date', 'url', 'parent', 'published', 'featured']
    date_hierarchy = 'source_date'

    
class VideoAdmin(AttachmentAdmin):
    fieldsets = [
        (None, {
            'fields': ['object_type', 'title', 'url', 'creator', 'published', 'publish_date', 'featured']
        }),
        ('Parent', {
            'fields': ['content_type', 'object_id', 'position']
        })
    ]
    list_display = ['title', 'object_type', 'parent', 'published', 'featured']
    list_editable = ['published', 'featured']
    

admin.site.register(Image, ImageAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Video, VideoAdmin)

