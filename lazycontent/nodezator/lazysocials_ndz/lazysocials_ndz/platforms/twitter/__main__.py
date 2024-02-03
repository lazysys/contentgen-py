from lazysocials.platforms import Twitter
from lazysocials.platforms.twitter import TwitterAuth

from lazycommon.content.types import Content

from typing import Type

main_callable = Twitter

def _Twitter(auth: TwitterAuth, *types: Type[Content], max_images: {"widget_name": "int_float_entry", "widget_kwargs": {"min_value": 0, "max_value": 4}, "type": int} = 4) -> [{"name": "twitter", "type": Twitter}]:
	pass

signature_callable = _Twitter
