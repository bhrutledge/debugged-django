from django.conf import settings

IMAGE_TYPES = getattr(settings, "DEBUGGED_IMAGE_TYPES", 
                     [('photo', 'Photo'), ('miscellaneous', 'Miscellaneous')])

FILE_TYPES = getattr(settings, "DEBUGGED_FILE_TYPES", 
                     [('audio', 'Audio'), ('download', 'Download'), ('miscellaneous', 'Miscellaneous')])

LINK_TYPES = getattr(settings, "DEBUGGED_LINK_TYPES", 
                     [('article', 'Article'), ('press', 'Press'), ('photos', 'Photos'), ('video', 'Video'), ('miscellaneous', 'Miscellaneous')])

VIDEO_TYPES = getattr(settings, "DEBUGGED_VIDEO_TYPES", 
                      [('live', 'Live'), ('music-video', 'Music Video'), ('miscellaneous', 'Miscellaneous')])
                      
VIDEO_SOURCES = getattr(settings, "DEBUGGED_VIDEO_SOURCES",
                        [(r'youtube\.com/watch\?v=(.*)$', 'YouTube'),
                         (r'vimeo\.com/(.*)$', 'Vimeo')])