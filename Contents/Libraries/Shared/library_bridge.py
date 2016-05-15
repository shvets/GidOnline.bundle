class LibraryBridge():
    def __init__(self):
        self.objects = {}

    def export_object(self, name, object):
        if name not in self.objects.keys():
            self.objects[name] = object

    def export_objects(self, objects):
        for name, object in objects.iteritems():
            self.export_object(name, object)

bridge = LibraryBridge()