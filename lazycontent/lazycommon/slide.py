
@dataclass
class Slide:
	caption: str
	headline: bool = False
	images: List[BufferedReader] = []
	
