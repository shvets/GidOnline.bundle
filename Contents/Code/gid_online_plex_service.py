from gid_online_service import GidOnlineService
from gid_online_plex_storage import GidOnlinePlexStorage

class GidOnlinePlexService(GidOnlineService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'gidonline.storage'))

        self.queue = GidOnlinePlexStorage(storage_name)

        self.queue.register_simple_type('movie')
        self.queue.register_simple_type('episode')
        self.queue.register_simple_type('season')
        self.queue.register_simple_type('serie')