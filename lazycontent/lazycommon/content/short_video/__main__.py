from ...content_type import ShortVideo

main_callable = ShortVideo

def _ShortVideo(content: {"widget_name": "text_display", "type": str} = "", video: bytes = b'') -> [{"name": "content", "type": ShortVideo}]:
	pass

signature_callable = _ShortVideo
