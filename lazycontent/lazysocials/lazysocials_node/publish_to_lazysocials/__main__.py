from ... import LazySocials
from lazycommon.content.types import Content

def publish_to_lazysocials(lazysocials: LazySocials, *contents: Content) -> [{"name": "lazysocials", "type": LazySocials}]:
	for content in contents:
		lazysocials.publish(content)
	return lazysocials

main_callable = publish_to_lazysocials

