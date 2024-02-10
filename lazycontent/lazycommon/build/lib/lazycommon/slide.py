from dataclasses import dataclass, field

from typing import List

from io import BufferedReader

@dataclass
class Slide:
	caption: str
	headline: bool = False
	images: List[BufferedReader] = field(default_factory=list)
	
