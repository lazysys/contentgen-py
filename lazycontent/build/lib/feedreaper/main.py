import os
from dotenv import load_dotenv

from feedreaper.feedreaper import FeedReaper, StorageConfig

load_dotenv()

storage_config = StorageConfig(os.getenv("FEEDS_FILE"), os.getenv("USED_FILE"))

reaper = FeedReaper(storage_config)

post = next(reaper)

print(post)
