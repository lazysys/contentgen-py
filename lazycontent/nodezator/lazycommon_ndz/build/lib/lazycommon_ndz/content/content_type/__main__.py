import inspect
import importlib

from lazycommon.content import types as content_types

types = [obj for name, obj in inspect.getmembers(content_types) if inspect.isclass(obj)]

def content_type(typ: {
	"name": "type",
	"widget_name": "option_menu",
	"widget_kwargs": {
		"options": [typ.__name__ for typ in types],
	},
	"type": str } = types[0].__name__
) -> [{ "name": "type", "type": content_types.Content }]:
	return next(filter(lambda x: x.__name__ == typ, types), None)

main_callable = content_type
