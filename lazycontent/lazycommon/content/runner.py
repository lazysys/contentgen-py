
from ..runner import Runner
from .types import Content

R = TypeVar("R")
class ContentRunner(Runner[Content, R]):
	def run(self, content: Content) -> R:
		self.run(type(Content), content)
