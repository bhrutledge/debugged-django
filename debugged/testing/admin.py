from django.contrib import admin
from django.contrib.contenttypes import generic

from debugged.testing.models import Parent, Attachment, GenericAttachment

class AttachmentInline(admin.TabularInline):
    model = Attachment

class GenericAttachmentInline(generic.GenericTabularInline):
    model = GenericAttachment
    
class ParentAdmin(admin.ModelAdmin):
    inlines = [AttachmentInline, GenericAttachmentInline]

admin.site.register(Attachment, admin.ModelAdmin)
admin.site.register(GenericAttachment, admin.ModelAdmin)
admin.site.register(Parent, ParentAdmin)