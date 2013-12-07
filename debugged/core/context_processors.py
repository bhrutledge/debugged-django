from django.contrib.sites.models import Site

def current_site(request):
    try:
        current_site = Site.objects.get_current()
    except Site.DoesNotExist:
        current_site = ''

    return {'current_site': current_site}
