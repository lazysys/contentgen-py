import os
from dotenv import load_dotenv

from feedreaper.feedreaper import FeedReaper, StorageConfig
from lazycommon.content_type import ContentType

load_dotenv()

storage_config = StorageConfig(os.getenv("FEEDS_FILE"), os.getenv("USED_FILE"))
openai_key = os.getenv("OPENAI_KEY")
types = [ContentType.MICROBLOG]

reaper = FeedReaper(storage_config, openai_key, types)

post = next(reaper)

print(post)
