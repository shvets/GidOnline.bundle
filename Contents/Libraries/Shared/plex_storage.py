import json

from media_info_storage import MediaInfoStorage

import library_bridge

Core = library_bridge.bridge.objects['Core']
DirectoryObject = library_bridge.bridge.objects['DirectoryObject']
Callback = library_bridge.bridge.objects['Callback']
L = library_bridge.bridge.objects['L']
R = library_bridge.bridge.objects['R']

ADD_ICON = 'icon-add.png'
REMOVE_ICON = 'icon-remove.png'

class PlexStorage(MediaInfoStorage):
    def __init__(self, file_name):
        MediaInfoStorage.__init__(self, file_name)

        self.storage = Core.storage

        self.load()

    def exist(self):
        return self.storage.file_exists(self.file_name)

    def load_storage(self):
        return json.loads(self.storage.load(self.file_name))

    def save_storage(self, data):
        self.storage.save(self.file_name, json.dumps(self.data, indent=4))

    def handle_bookmark_operation(self, operation, media_info):
        if operation == 'add':
            self.add(media_info)
        elif operation == 'remove':
            self.remove(media_info)

    def append_bookmark_controls(self, oc, handler, media_info):
        bookmark = self.find(media_info)

        if bookmark:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='remove', **media_info),
                title=unicode(L('Remove Bookmark')),
                thumb=R(REMOVE_ICON)
            ))
        else:
            oc.add(DirectoryObject(
                key=Callback(handler, operation='add', **media_info),
                title=unicode(L('Add Bookmark')),
                thumb=R(ADD_ICON)
            ))
