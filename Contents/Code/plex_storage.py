import constants
from storage import Storage

class PlexStorage(Storage):
    def __init__(self, file_name):
        Storage.__init__(self, Core.storage, file_name)

        self.load()

    def append_controls(self, oc, media_info, add_bookmark_handler, remove_bookmark_handler):
        bookmark = self.get_bookmark(media_info)

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(remove_bookmark_handler, **media_info),
                title=unicode(L('Remove Bookmark')),
                thumb=R(constants.REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(add_bookmark_handler, **media_info),
                title=unicode(L('Add Bookmark')),
                thumb=R(constants.ADD_ICON)
            ))

    def add_bookmark(self, media_info):
        self.add(media_info)

        self.save()

    def remove_bookmark(self, media_info):
        self.remove(media_info)

        self.save()

    def get_bookmark(self, media_info):
        found = None

        for item in self.data:
            if 'path' in media_info:
                if 'path' in item and item['path'] == media_info['path']:
                    if 'season' in media_info:
                        if 'season' in item and item['season'] == media_info['season']:
                            if 'episode' in media_info:
                                if 'episode' in item and item['episode'] == media_info['episode']:
                                    found = item
                                    break
                            else:
                                found = item
                                break
                    else:
                        found = item
                        break

        return found