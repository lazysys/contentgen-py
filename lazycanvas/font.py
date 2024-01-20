from dataclasses import dataclass
from enum import Enum, auto
import os

from PIL import ImageFont

class FontType(Enum):
	NORMAL = "normal"
	ITALIC = "italic"
	BOLD = "bold"

@dataclass
class Font:
	root: str
	name: str

	def get(self, size: int, typ: FontType = FontType.NORMAL) -> ImageFont:
		root = os.path.join(self.root, self.name)
		files = [file for file in os.listdir(root) if file.endswith(".ttf")]
		font = None
		for file in files:
			if typ.value.lower() in file.lower():
				font = os.path.join(root, file)
		return ImageFont.truetype(font or os.path.join(root, files[0]), size)
