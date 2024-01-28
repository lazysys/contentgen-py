import inspect
from ...content_type import Content
from ... import content_type

types = [obj for name, obj in inspect.getmembers(content_type) if inspect.isclass(obj)]
types.remove(Content)

def content_type_picker(type: {
	"widget_name": "option_menu",
	"widget_kwargs": {
		"options": [type.__name__ for type in types],
	},
	"type": str
} = types[0].__name__) -> [{ "name": "type", "type": Content }]:
	return next(filter(lambda x: x.__name__ == type, types), None)

main_callable = content_type_picker
