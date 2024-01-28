from .. import Twitter
from ..twitter import TwitterAuth

import lazycommon.content_type as content

from typing import Type

def twitter(auth: TwitterAuth, *types: Type[content.Content]) -> [{"name": "twitter", "type": Twitter}]:
	return Twitter(auth, types)

main_callable = twitter
