from ...content_type import Video

main_callable = Video

def _Video(content: {"widget_name": "text_display", "type": str} = "", video: bytes = b'') -> [{"name": "content", "type": Video}]:
	pass

signature_callable = _Video
