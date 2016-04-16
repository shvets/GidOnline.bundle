import constants
from storage import Storage

class PlexStorage(Storage):
    def __init__(self, file_name):
        Storage.__init__(self, Core.storage, file_name)

        self.load()

    def append_controls(self, oc, handler, **params):
        bookmark = self.get_bookmark(**params)

        if bookmark:
            params['operation'] = 'remove'
            oc.add(DirectoryObject(
                key=Callback(handler, **params),
                title=unicode(L('Remove Bookmark')),
                thumb=R(constants.REMOVE_ICON)
            ))
        else:
            params['operation'] = 'add'
            oc.add(DirectoryObject(
                key=Callback(handler, **params),
                title=unicode(L('Add Bookmark')),
                thumb=R(constants.ADD_ICON)
            ))

    def add_bookmark(self, **params):
        self.add(**params)

        self.save()

    def remove_bookmark(self, **params):
        self.remove(**params)

        self.save()

    def get_bookmark(self, **params):
        found = None

        for item in self.data:
            if 'path' in params:
                if 'path' in item and item['path'] == params['path']:
                    if 'season' in params:
                        if 'season' in item and item['season'] == params['season']:
                            if 'episode' in params:
                                if 'episode' in item and item['episode'] == params['episode']:
                                    found = item
                                    break
                            else:
                                found = item
                                break
                    else:
                        found = item
                        break

        return found