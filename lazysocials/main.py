from lazysocials.lazysocials import LazySocials
from lazysocials.twitter import Twitter, TwitterAuth

from feedreaper.rssfeed import Entry

from lazycommon.content_type import ContentType

import os
from dotenv import load_dotenv

load_dotenv()

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

lazysocials.publish(
	(
		Entry({ "link": "google.com" }), 
		{
			ContentType.MICROBLOG: ["test"]
		}
	)
)
