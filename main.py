import os
from dotenv import load_dotenv

from feedreaper.feedreaper import FeedReaper, StorageConfig

from lazysummary.openai import OpenAISummarizer, OpenAIChat

from lazycommon.content_type import *


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
from lazysocials.lazysocials import LazySocials

'''
from lazysocials.platforms.twitter import Twitter, TwitterAuth
twitter = Twitter(
	TwitterAuth(
		consumer_key = os.getenv("TWITTER_CONSUMER_KEY"),
		consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"),
		access_token = os.getenv("TWITTER_ACCESS_TOKEN"),
		access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
	),
	types = [Microblog, Image, Carousel]
)
'''

'''
from lazysocials.platforms.reddit import Reddit, RedditAuth
reddit = Reddit(
	RedditAuth(
		client_id = os.getenv("REDDIT_CLIENT_ID"),
		client_secret = os.getenv("REDDIT_CLIENT_SECRET"),
		username = os.getenv("REDDIT_USERNAME"),
		password = os.getenv("REDDIT_PASSWORD"),
		user_agent = "LazyContent (by u/gregismotion)",
	),
	{"StableDiffusion": "News", "technology": "Artificial Intelligence", "artificial": "News"},
	types = [Microblog]
)
'''

from lazysocials.platforms.Local import Local
local = Local("local")

platforms = [local]
lazysocials = LazySocials(platforms)

entry = None
while not entry:
	entry = next(feedreaper)

# FIXME: wbu duplicate images?
images = [entry.thumbnail] + entry.images + entry.related_images

microblog = summarizer.summarize([entry], Microblog)
microblog = Microblog(microblog, images)

thread = summarizer.summarize([entry], Thread)
thread = Thread(thread[0], Microblog(microblog, images))

images = [lazycanvas.master_slide(summary[0])] + [lazycanvas.carousel_slide(text, i) for i, text in enumerate(summary)]
files = list(map(lazycanvas.get_temp_file, images))

content = Carousel(content = summary[0], images = [Image(text, file) for text, file in zip(summary, files)])

lazysocials.publish(content)
