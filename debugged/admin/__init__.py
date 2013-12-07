from django.contrib import admin
from django.contrib.contenttypes import generic

class LinkedStackedInline(admin.StackedInline):
    template = 'admin/edit_inline/stacked_linked.html'

class LinkedTabularInline(admin.TabularInline):
    template = 'admin/edit_inline/tabular_linked.html'

class GenericLinkedStackedInline(generic.GenericStackedInline):
    template = 'admin/edit_inline/stacked_linked.html'

class GenericLinkedTabularInline(generic.GenericTabularInline):
    template = 'admin/edit_inline/tabular_linked.html'
