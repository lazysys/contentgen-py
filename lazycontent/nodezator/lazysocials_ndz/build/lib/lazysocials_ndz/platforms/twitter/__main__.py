from .. import Twitter
from ..twitter import TwitterAuth

from lazycommon.content.types import Content

from typing import Type

def twitter(auth: TwitterAuth, *types: Type[Content]) -> [{"name": "twitter", "type": Twitter}]:
	return Twitter(auth, types)

main_callable = twitter
