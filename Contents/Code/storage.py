import json
import copy

class Storage:
    def __init__(self, storage, file_name):
        self.storage = storage
        self.file_name = file_name

        self.clear()

    def clear(self):
        self.data = []

    def storage_exist(self):
        return self.storage.file_exists(self.file_name)

    def load(self):
        self.clear()

        if self.storage_exist():
            self.data = json.loads(self.storage.load(self.file_name))

    def save(self, data=None):
        if data:
            self.data = copy.copy(data)

        self.storage.save(self.file_name, json.dumps(self.data, indent=4))

    def add(self, **params):
        self.data.append(params)

    def remove(self, **params):
        self.data.remove(params)