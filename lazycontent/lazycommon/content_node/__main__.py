import inspect
from ..content_type import Content
from .. import content_type

types = [obj for name, obj in inspect.getmembers(content_type) if inspect.isclass(obj)]
types.remove(Content)

def content_type_picker(typ: {
	"widget_name": "option_menu",
	"widget_kwargs": {
		"options": types,
	},
	"type": Content
}) -> Content:
	return typ

main_callable = content_type_picker
