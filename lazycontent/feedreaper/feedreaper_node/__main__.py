from ..feedreaper import FeedReaper
from ..storage import StorageConfig

main_callable = FeedReaper

def _FeedReaper(storage_config: StorageConfig) -> [{"name": "reaper", "type": FeedReaper}]:
	pass

signature_callable = _FeedReaper
