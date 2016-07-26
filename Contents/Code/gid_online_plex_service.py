from gid_online_service import GidOnlineService
from plex_storage import PlexStorage
#import plex_util

class GidOnlinePlexService(GidOnlineService):
    def __init__(self):
        storage_name = Core.storage.abs_path(Core.storage.join_path(Core.bundle_path, 'Contents', 'gidonline.storage'))

        self.queue = PlexStorage(storage_name)

        self.queue.register_simple_type('movie')
        self.queue.register_simple_type('episode')
        self.queue.register_simple_type('season')
        self.queue.register_simple_type('serie')

        #self.set_proxy(plex_util.get_proxy(), plex_util.get_proxy_type())
