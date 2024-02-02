from ...content_type import Article

main_callable = Article

def _Article(content: {"widget_name": "text_display", "type": str} = "", title: str = "") -> [{"name": "content", "type": Article}]:
	pass

signature_callable = _Article
