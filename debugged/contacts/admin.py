from django.contrib import admin
from django.conf import settings

from debugged.contacts.models import Location, Contact


class LocationAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': ['name', 'object_type', 'website', 'description']
        }),
        ('Address', {
            'fields': ['address_1', 'address_2', 'city', 'region', 'postal_code', 'country']
        })
    ]
    
    list_display = ['name', 'object_type', 'city', 'region']
    list_filter = ['object_type']
    search_fields = ['name', 'city']
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']

  
class ContactAdmin(admin.ModelAdmin):
    fields = ['name', 'object_type', 'website', 'description']
    list_display = ['name', 'object_type']
    list_filter = ['object_type']
    search_fields = ['name']
    
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']
    

admin.site.register(Location, LocationAdmin)
admin.site.register(Contact, ContactAdmin)
