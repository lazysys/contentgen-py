from lazycommon.content_type import *

def main():
	# Load environment configuration
	import os
	from dotenv import load_dotenv
	load_dotenv()
	branding = os.getenv("BRANDING")

	# FeedReaper
	from feedreaper.feedreaper import FeedReaper, StorageConfig
	storage_config = StorageConfig(os.getenv("FEEDS_FILE"), os.getenv("USED_FILE"))
	feedreaper = FeedReaper(storage_config)

	# LazySummary
	from lazysummary.openai import OpenAISummarizer, OpenAIChat
	key = os.getenv("OPENAI_KEY")
	api = OpenAIChat(key)
	summarizer = OpenAISummarizer(api)

	# LazyCanvas
	from lazycanvas.lazycanvas import LazyCanvas
	from lazycanvas.templates.folder import FolderTemplate
	template = FolderTemplate(os.getenv("LAZYCANVAS_TEMPLATE_FOLDER"))
	lazycanvas = LazyCanvas(template, f"@{branding}")

	# LazyVideo
	# TODO: implement

	# LazySocials
	from lazysocials.lazysocials import LazySocials

	from lazysocials.platforms.twitter import Twitter, TwitterAuth
	twitter = Twitter(
		TwitterAuth(
			consumer_key = os.getenv("TWITTER_CONSUMER_KEY"),
			consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET"),
			access_token = os.getenv("TWITTER_ACCESS_TOKEN"),
			access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
		),
		types = [Microblog, Thread, Image]
	)

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

	from lazysocials.platforms.local import Local
	local = Local(_root = "local", types = [Microblog, Thread, Article, Image, Carousel, Video])

	platforms = [local, twitter, reddit]
	lazysocials = LazySocials(platforms)

	print("All initialized.")

	entry = None
	while not entry:
		entry = next(feedreaper)
	print("Entry picked!")


	print("Start downloading images...")
	images = [] if not entry.thumbnail else [entry.thumbnail] 
	print("Got images!")

	microblog = summarizer.summarize([entry], Microblog)
	microblog = Microblog(microblog[0], images = images)
	print("Microblog done.")

	thread = summarizer.summarize([entry], Thread)
	thread = Thread(thread[0], microblogs = [Microblog(content) for content in thread[1:]], images = images)
	print("Thread done.")

	'''
	article = summarizer.summarize([entry], Article)
	article = Article(title = article[0], content = article[1])

	print("Article done.")
	'''

	image = summarizer.summarize([entry], Image)
	slide = lazycanvas.master_slide(image[0])
	slide = lazycanvas.get_temp_file(slide)
	image = Image(image[0], slide)
	print("Image done.")

	carousel = summarizer.summarize([entry], Carousel)
	slides = [lazycanvas.master_slide(carousel[0])] + [lazycanvas.carousel_slide(text, i) for i, text in enumerate(carousel[1:])]
	carousel_files = list(map(lazycanvas.get_temp_file, slides))
	carousel = Carousel(content = carousel[0], images = [Image(text, file) for text, file in zip(carousel, carousel_files)])
	print("Carousel done.")

	print("Start publishing...")

	#content = [microblog, thread, article, image, carousel]
	content = [microblog, thread, image, carousel]
	list(map(lazysocials.publish, content))

	print("All published!")

if __name__ == "__main__":
    main()
