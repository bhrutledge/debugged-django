from datetime import datetime
from debugged.stream.signals import update_stream_item, delete_stream_item

def update_featured_stream_item(sender, instance, **kwargs):
    if instance.featured:
        update_stream_item(sender, instance)
    else:
        delete_stream_item(sender, instance)

def set_publish_date(sender, instance, **kwargs):
    instance.modify_date = datetime.now()
    
    if not instance.published:
        instance.publish_date = None
    elif not instance.publish_date:
        instance.publish_date = instance.modify_date
            
    if not instance.featured:
        instance.feature_date = None
    elif not instance.feature_date:
        instance.feature_date = instance.modify_date

def set_position(sender, instance, **kwargs):
    if not instance.position:
        instance_filter = instance._get_position_filter()
        instance_objects = instance.__class__.objects.filter(instance_filter)
        try:
            instance.position = instance_objects.order_by('-position')[0].position + 1
        except:
            instance.position = 1        

