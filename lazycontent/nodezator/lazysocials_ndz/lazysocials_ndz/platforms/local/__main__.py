from lazysocials.platforms import Local

from lazycommon.content.types import Content

from typing import Type

main_callable = Local

def _Local(root: { "widget_name": "path_preview", "type": str } = ".", *types: Type[Content]) -> [{"name": "local", "type": Local}]:
	pass

signature_callable = _Local

