from gid_online_service import GidOnlineService
from plex_storage import PlexStorage

class PlexService(GidOnlineService):
     def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'gidonline.storage'))

        self.queue = PlexStorage(storage_name)