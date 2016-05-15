import json

from media_info_storage import MediaInfoStorage

import library_bridge

Core = library_bridge.bridge.objects['Core']

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
