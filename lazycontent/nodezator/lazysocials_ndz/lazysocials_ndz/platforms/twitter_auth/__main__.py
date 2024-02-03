from lazysocials.platforms.twitter import TwitterAuth

main_callable = TwitterAuth

def _TwitterAuth(consumer_key: str = "", consumer_secret: str = "", access_token: str = "", access_token_secret: str = "") -> [{"name": "twitter_auth", "type": TwitterAuth}]:
	pass

signature_callable = _TwitterAuth
