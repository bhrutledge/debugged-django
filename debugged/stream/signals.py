from datetime import datetime, timedelta
from django.contrib.contenttypes.models import ContentType
from debugged.stream.models import StreamEntry, StreamItem

def _get_stream_item(instance):
    instance_type = ContentType.objects.get_for_model(instance)

    try:
        s = StreamItem.objects.get(content_type=instance_type, object_id=instance.id)
    except:
        s = StreamItem(content_type=instance_type, object_id=instance.id)

    return s

def _get_stream_entry(instance):
    instance_type = ContentType.objects.get_for_model(instance)
    
    try:
        parent = instance.parent
        parent_type = ContentType.objects.get_for_model(parent)
        parent_id = parent.id
    except:
        parent = parent_type = parent_id = None

    end_date = instance.publish_date + timedelta(minutes=30)
    start_date = instance.publish_date - timedelta(minutes=30)
    
    try:
        e = StreamEntry.objects.get(item_type=instance_type, 
                                    content_type=parent_type, object_id=parent_id,
                                    publish_date__range=(start_date, end_date))
    except:
        e = StreamEntry(item_type=instance_type,
                        content_type=parent_type, object_id=parent_id)
                        
    return e
    
def delete_stream_item(sender, instance, **kwargs):
    instance_type = ContentType.objects.get_for_model(instance)
    try:
        item = StreamItem.objects.get(content_type=instance_type.id, object_id=instance.id)
        entry = item.entry
        item.delete()
        
        if entry.items.count() == 0:
            entry.delete()
    except:
        pass
                
def update_stream_item(sender, instance, **kwargs):
    # TODO: What about StreamItems that already have StreamEntries?
    if instance.published:
        item = _get_stream_item(instance)
        entry = _get_stream_entry(instance)
        
        if entry.publish_date:
            entry.publish_date = max(instance.publish_date, entry.publish_date)
        else:
            entry.publish_date = instance.publish_date

        entry.modify_date = datetime.now()
        entry.save()
        
        try:
            old_entry = item.entry
        except:
            old_entry = None

        item.publish_date = instance.publish_date
        item.modify_date = instance.modify_date
        item.entry = entry
        item.save()    
        
        if old_entry and old_entry.items.count() == 0:
            old_entry.delete()
    else:
        delete_stream_item(sender, instance)
