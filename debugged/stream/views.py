from django.views.generic import list_detail
from debugged.stream.models import StreamEntry

def entries(request, paginate_by=10, page=None, template_name=None,
            extra_context=None, template_object_name='entry'):

    return list_detail.object_list(request,
        queryset=StreamEntry.objects.order_by('-publish_date'),
        paginate_by=paginate_by,
        page=page,
        template_name=template_name,
        template_object_name=template_object_name,
        extra_context=extra_context)
