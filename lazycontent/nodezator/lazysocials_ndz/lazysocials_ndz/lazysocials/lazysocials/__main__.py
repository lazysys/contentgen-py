from lazysocials import LazySocials
from lazysocials.platforms import Platform

def lazysocials(*platforms: Platform) -> [{"name": "lazysocials", "type": LazySocials}]:
	return LazySocials(platforms)

main_callable = lazysocials
