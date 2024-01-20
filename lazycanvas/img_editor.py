from PIL import Image, ImageDraw

from dataclasses import dataclass
from typing import Tuple

from font import Font, FontType

@dataclass
class PointCalculator:
	image: Image

	@property
	def top_text(self) -> Tuple[int, int]:
		return (self.image.width/2, self.image.height*0.075)

	@property
	def bottom_text(self) -> Tuple[int, int]:
		return (self.image.width/2, self.image.height*(1-0.075))
	
	@property
	def body_constraints(self) -> Tuple[int, int, int, int]:
		offset_y = self.image.height*0.1
		offset_x = self.image.width*0.1
		return (offset_x, self.top_text[1] + offset_y, self.image.width - offset_x, self.bottom_text[1] - offset_y)

@dataclass
class ImageEditor:
	image: Image
	
	@property
	def points(self) -> PointCalculator:
		return PointCalculator(self.image)
	
	def _offset_bbox(self, bbox: Tuple[int, int, int, int], x: int, y: int):
		return [bbox[0] + x, bbox[1] + y, bbox[2] + x, bbox[3] + y]
	def _is_bbox_valid(self, bbox: Tuple[int, int, int, int]):
		return not (any(elem < 0 for elem in bbox) or (bbox[0] > self.image.width or bbox[2] > self.image.width) or (bbox[1] > self.image.height or bbox[3] > self.image.height))
	def _is_bbox_within_constraints(self, bbox: Tuple[int, int, int, int], constraints: Tuple[int, int, int, int]):
		return not any(bbox[i] > (constraints[i] or (self.image.width if i % 2 == 0 else self.image.height)) for i in range(len(bbox)))

	def write_text(self, text: str, 
		size: int,
		font: Font,
		center: Tuple[int, int] = None, 
		constraints: Tuple[int, int, int, int] = (None, None, None, None),
		color: Tuple[int, int, int] = (255, 255, 255),
		line_spacing: int = 50, 
	) -> Tuple[int, int, int, int]:
		image = self.image.copy()
		draw = ImageDraw.Draw(image)
		
		_font = font.get(size, FontType.NORMAL)

		if center is None:
			x = image.width / 2
			y = image.height / 2
		else:
			x, y = center

		lines = []
		line = ""
		for word in text.split():
			bbox = draw.textbbox((0, 0), line + word, font = _font)
			if self._is_bbox_valid(bbox) and self._is_bbox_within_constraints(bbox, constraints):
				line += word + " "
			else:
				lines.append(line.strip())
				line = word + " "
		lines.append(line.strip())
		
		total_height = sum(draw.textbbox((0, 0), line, font = _font)[3] + line_spacing for line in lines)
		if total_height > ((constraints[3] or image.height) - (constraints[1] or 0)):
			return self.write_text(text=text, center=center, constraints=constraints, line_spacing=line_spacing, size = size - 1, color=color, font=font)

		y -= total_height / 2

		result = [0, 0, 0, 0]
		count = 0
		
		for line in lines:
			bbox = draw.textbbox((0, 0), line, font = _font)
			
			# NOTE: this is probably useless(?), plus breaks stuff
			#if not (self._is_bbox_valid(bbox) and self._is_bbox_within_constraints(bbox, constraints)):
			#	return self.write_text(text=text, center=center, constraints=constraints, line_spacing=line_spacing, size = size - 1, color=color, font=font)

			if count == 0:
				result[0] = bbox[0]
				result[1] = bbox[1]
			elif count == len(lines) - 1:
				result[2] = bbox[2]
				result[3] = bbox[3]

			x = (image.width - bbox[2]) // 2
			draw.text((x, y), line, font = _font, fill = color)
			y += bbox[3] + line_spacing
			count += 1
		
		self.image = image
		return tuple(result)
