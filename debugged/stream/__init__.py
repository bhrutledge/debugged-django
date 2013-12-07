from django.db.models.signals import post_save, pre_delete

from debugged.core.utils import get_model, get_callback
from debugged.stream.settings import STREAM_ITEMS
from debugged.stream.signals import update_stream_item, delete_stream_item


for item in STREAM_ITEMS:
    model_path = item
    update_callback = update_stream_item
    delete_callback = delete_stream_item

    if isinstance(item, (list, tuple)):
        model_path = item[0]
        try:
            update_callback = get_callback(item[1])
            delete_callback = get_callback(item[2])
        except IndexError:
            pass

    model = get_model(model_path)
    post_save.connect(update_callback, sender=model)
    pre_delete.connect(delete_callback, sender=model)