from storage import Storage

class PlexStorage(Storage):
    def __init__(self, file_name):
        Storage.__init__(self, file_name)

        self.load()

    def storage_exist(self):
       return Core.storage.file_exists(self.file_name)

    def storage_load(self):
       return Core.storage.load(self.file_name)

    def storage_save(self, new_data):
        Core.storage.save(self.file_name, new_data)