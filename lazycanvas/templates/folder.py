from typing import Tuple
from dataclasses import dataclass
import os

from PIL import Image
import yaml

from templates.templates import CanvasTemplate

from font import Font

@dataclass
class FolderTemplate(CanvasTemplate):
	_path: str
	
	@property
	def path(self):
		return self._path
	@path.setter
	def path(self, new: str):
		self._path = new
		self.__post_init__()
	
	def __post_init__(self):
		with open(os.path.join(self.path, "conf.yaml"), "r") as file:
			self.data = yaml.safe_load(file)

	@property
	def backgrounds(self):
		return tuple(map(Image.open, [os.path.join(self.path, "backgrounds", f"{i}.png") for i in range(3)]))
	
	@property
	def colors(self):
		return (tuple(self.data["colors"]["primary"]), tuple(self.data["colors"]["secondary"]))
	
	@property
	def fonts(self):
		root = os.path.join(self.path, "fonts")
		return (Font(root, self.data["fonts"]["primary"]), Font(root, self.data["fonts"]["secondary"]))
	
	@property
	def sizes(self):
		return self.data["sizes"]
