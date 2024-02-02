
from lazycommon.content.runner import ContentRunner
from lazycommon.content.types import Content

class Platform(ContentRunner[bool]):
	def publish(self, content: Content) -> bool:
		return self.run(content)
