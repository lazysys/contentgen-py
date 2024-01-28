from .. import Local

import lazycommon.content_type as content

from typing import Type

def local(root: { "widget_name": "path_preview", "type": str } = ".", *types: Type[content.Content]) -> [{"name": "local", "type": Local}]:
	return Local(_root = root, types = types)

main_callable = local
