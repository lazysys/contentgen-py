from ..runner import Runner
from .types import Content

from typing import TypeVar

R = TypeVar("R")
class ContentRunner(Runner[Content, R]):
	def run(self, content: Content) -> R:
		return super().run(type(content), content)
