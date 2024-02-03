from lazycommon.content.types import Image

from io import BufferedReader

main_callable = Image

def _Image(content: {"widget_name": "text_display", "type": str} = "", image: BufferedReader = None) -> [{"name": "content", "type": Image}]:
	pass

signature_callable = _Image
