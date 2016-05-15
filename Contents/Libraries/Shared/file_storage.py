import json
import os.path

from storage import Storage

class FileStorage(Storage):
    def __init__(self, file_name):
        Storage.__init__(self)

        self.file_name = file_name

    def exist(self):
        return os.path.exists(self.file_name)

    def load_storage(self):
        return json.loads(file.read(open(self.file_name, "r")))

    def save_storage(self, data):
        open(self.file_name, "w").write(json.dumps(data, indent=4))
