from .. import Local

from lazycommon.content.types import Content

from typing import Type

def local(root: { "widget_name": "path_preview", "type": str } = ".", *types: Type[Content]) -> [{"name": "local", "type": Local}]:
	return Local(_root = root, types = types)

main_callable = local
