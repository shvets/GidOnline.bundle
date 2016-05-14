import constants
from plex_storage import PlexStorage

class GidOnlinePlexStorage(PlexStorage):
    def __init__(self, file_name):
        PlexStorage.__init__(self, Core.storage, file_name)

        self.load()

    def append_controls(self, oc, handler, media_info):
        bookmark = self.find(media_info)

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='remove', **media_info),
                title=unicode(L('Remove Bookmark')),
                thumb=R(constants.REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='add', **media_info),
                title=unicode(L('Add Bookmark')),
                thumb=R(constants.ADD_ICON)
            ))
