import os
from dotenv import load_dotenv

from feedreaper.feedreaper import FeedReaper, StorageConfig

from lazysummary.openai import OpenAISummarizer, OpenAIChat

from lazycommon.content_type import *

from lazysocials.lazysocials import LazySocials
from lazysocials.platforms.twitter import Twitter, TwitterAuth
from lazysocials.platforms.reddit import Reddit, RedditAuth

from lazycanvas.lazycanvas import LazyCanvas
from lazycanvas.templates.folder import FolderTemplate

load_dotenv()

branding = os.getenv("BRANDING")

# FeedReaper
storage_config = StorageConfig(os.getenv("FEEDS_FILE"), os.getenv("USED_FILE"))
feedreaper = FeedReaper(storage_config)

# LazySummary
key = os.getenv("OPENAI_KEY")
api = OpenAIChat(key)
summarizer = OpenAISummarizer(api)

# LazyCanvas
template = FolderTemplate(os.getenv("LAZYCANVAS_TEMPLATE_FOLDER"))
lazycanvas = LazyCanvas(template, f"@{branding}")

# LazyVideo
# TODO: implement

# LazySocials
twitter = Twitter(
	TwitterAuth(
		consumer_key = os.getenv("TWITTER_CONSUMER_KEY"),
		consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"),
		access_token = os.getenv("TWITTER_ACCESS_TOKEN"),
		access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
	)
)
reddit = Reddit(
	RedditAuth(
		client_id = os.getenv("REDDIT_CLIENT_ID"),
		client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
		username = os.getenv("REDDIT_USERNAME"),
		password = os.getenv("REDDIT_PASSWORD"),
		user_agent = "LazyContent (by u/gregismotion)",
	),
	{"StableDiffusion": "News", "technology": "Artificial Intelligence", "artificial": "News"}
)
platforms = [twitter]
lazysocials = LazySocials(platforms)

entry = None
while not entry:
	entry = next(feedreaper)

summary = summarizer.summarize([entry], Image)
lazycanvas.master_slide(summary[0]).show()
#content = Image(content = summary[0], image = lazycanvas.master_slide(summary[0]))

#lazysocials.publish(content)
