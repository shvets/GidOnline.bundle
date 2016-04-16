import json

class Storage():
    def __init__(self, storage, file_name):
        self.storage = storage
        self.file_name = file_name

    def reset(self):
        self.data = []

    def storage_exist(self):
        return self.storage.file_exists(self.file_name)

    def load(self):
        self.reset()

        if self.storage_exist():
            self.data = json.loads(self.storage.load(self.file_name))

    def save(self, config=None):
        if config:
            for item in config.items():
                self.data.append(item)

        self.storage.save(self.file_name, json.dumps(self.data, indent=4))

    def add(self, item):
        self.data.append(item)

    def remove(self, item):
        self.data.remove(item)