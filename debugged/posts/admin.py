from django.contrib import admin
from django.conf import settings

from debugged.posts.models import Post
from debugged.attachments.admin import inlines as attachment_inlines


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'slug', 'author', 'body', 'published', 'publish_date', 'featured']
    prepopulated_fields = {'slug': ['title']}
    inlines = attachment_inlines
    list_display = ['title', 'publish_date', 'author', 'published', 'featured']
    ordering = ['-publish_date']
    list_editable = ['published', 'featured']
    list_filter = ['author', 'published', 'featured']
    date_hierarchy = 'publish_date'
    
    class Media:
        css = {'all': ['attachments/css/inline.css']}
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']

admin.site.register(Post, PostAdmin)
