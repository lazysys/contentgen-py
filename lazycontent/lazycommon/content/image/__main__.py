from ...content_type import Image

main_callable = Image

def _Image(content: {"widget_name": "text_display", "type": str} = "", image: {"widget_name": "image_preview", "type": str} = ".") -> [{"name": "content", "type": Image}]:
	pass

signature_callable = _Image
