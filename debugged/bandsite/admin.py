from django.contrib import admin
from django.conf import settings

from django.contrib.flatpages.models import FlatPage
from django.contrib.flatpages.admin import FlatPageAdmin
from flatblocks.models import FlatBlock
from flatblocks.admin import FlatBlockAdmin

class RichFlatPageAdmin(FlatPageAdmin):
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']
              
class RichFlatBlockAdmin(FlatBlockAdmin):
    class Media:
        js = [settings.ADMIN_MEDIA_PREFIX + 'tinymce/jscripts/tiny_mce/tiny_mce.js', 
              settings.STATIC_URL + 'js/tinymce_setup.js']

# TODO: Enable rich editors for flat content
# admin.site.unregister(FlatPage)
# admin.site.register(FlatPage, RichFlatPageAdmin)
# admin.site.unregister(FlatBlock)
# admin.site.register(FlatBlock, RichFlatBlockAdmin)
