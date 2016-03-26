import json
import os.path

class Storage():
    def __init__(self, file_name):
        self.file_name = file_name

        self.data = []

    def storage_exist(self):
        return os.path.exists(self.file_name)

    def storage_load(self):
        #return Core.storage.load(self.file_name)
        return ''

    def storage_save(self, new_data):
        #Core.storage.save(self.file_name, new_data)
        return ''

    def load(self):
        self.data = []

        if self.storage_exist():
            self.data = json.loads(self.storage_load())

    def save(self, config=None):
        if config:
            for item in config.items():
                self.data.append(item)

        self.storage_save(json.dumps(self.data, indent=4))

    def add(self, item):
        self.data.append(item)

    def remove(self, item):
        self.data.remove(item)