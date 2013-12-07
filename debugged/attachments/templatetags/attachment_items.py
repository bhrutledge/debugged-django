from django import template

register = template.Library()

@register.inclusion_tag('attachments/file_item.html')
def fileitem(attachment):
    return {'file': attachment}

@register.inclusion_tag('attachments/image_item.html')
def imageitem(attachment, gallery_id=''):
    return {'image': attachment, 'gallery_id': gallery_id}

@register.inclusion_tag('attachments/link_item.html')
def linkitem(attachment):
    return {'link': attachment}
    
@register.inclusion_tag('attachments/video_item.html')
def videoitem(attachment):
    return {'video': attachment}
    