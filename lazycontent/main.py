import os
from dotenv import load_dotenv

from feedreaper.feedreaper import FeedReaper, StorageConfig
from feedreaper.rssfeed import Entry
from feedreaper.summarizer import OpenAIChat, OpenAISummarizer

from lazycommon.content_type import ContentType

from lazysocials.lazysocials import LazySocials
from lazysocials.twitter import Twitter, TwitterAuth

load_dotenv()

# FeedReaper
storage_config = StorageConfig(os.getenv("FEEDS_FILE"), os.getenv("USED_FILE"))

openai = OpenAIChat(os.getenv("OPENAI_KEY"))
summarizer = OpenAISummarizer(openai)

types = [ContentType.MICROBLOG]

reaper = FeedReaper(storage_config, summarizer, types)

# LazySocials
twitter = Twitter(
	TwitterAuth(
		consumer_key = os.getenv("TWITTER_CONSUMER_KEY"),
		consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"),
		access_token = os.getenv("TWITTER_ACCESS_TOKEN"),
		access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
	)
)
platforms = [twitter]
lazysocials = LazySocials(platforms)

post = next(reaper)
lazysocials.publish(post)