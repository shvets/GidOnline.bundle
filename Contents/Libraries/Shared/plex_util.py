import library_bridge

L = library_bridge.bridge.objects['L']
Resource = library_bridge.bridge.objects['Resource']
Prefs = library_bridge.bridge.objects['Prefs']
Core = library_bridge.bridge.objects['Core']
Locale = library_bridge.bridge.objects['Locale']
MessageContainer = library_bridge.bridge.objects['MessageContainer']

def get_thumb(url, fallback=None):
    if fallback:
        thumb = Resource.ContentsOfURLWithFallback(url=url, fallback=fallback)
    else:
        thumb = Resource.ContentsOfURLWithFallback(url=url, fallback='icon-default.png')

    return thumb

def get_language():
    return Prefs['language'].split('/')[1]

def get_proxy():
    return Prefs['proxy']

def get_proxy_type():
    return Prefs['proxy_type']

def validate_prefs():
    language = get_language()

    if Core.storage.file_exists(Core.storage.abs_path(
        Core.storage.join_path(Core.bundle_path, 'Contents', 'Strings', '%s.json' % language)
    )):
        Locale.DefaultLocale = language
    else:
        Locale.DefaultLocale = 'en-us'

def no_contents(name=None):
    if not name:
        name = 'Error'

    return MessageContainer(header=unicode(L(name)), message=unicode(L('No entries found')))

def sanitize(name):
    return unicode(name[0:35])