from debugged.stream.signals import update_stream_item, delete_stream_item

def update_song_stream_item(sender, instance, **kwargs):
    if instance.audio:
        update_stream_item(sender, instance)
    else:
        delete_stream_item(sender, instance)
