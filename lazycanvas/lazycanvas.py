from PIL import Image, ImageDraw, ImageFont

from dataclasses import dataclass
from typing import Tuple

@dataclass
class PointCalculator:
	image: Image

	@property
	def top_text(self) -> Tuple[int, int]:
		return (self.image.width/2, self.image.height*0.075)

	@property
	def bottom_text(self) -> Tuple[int, int]:
		return (self.image.width/2, self.image.height*(1-0.075))

@dataclass
class ImageEditor:
	image: Image
	
	@property
	def points(self) -> PointCalculator:
		return PointCalculator(self.image)
	
	def write_text(self, text: str, 
		center: Tuple[int, int] = None, 
		constraints: Tuple[int, int] = (None, None), 
		line_spacing: int = 50, 
		size: int = 275, 
		color: Tuple[int, int, int] = (255, 255, 255)
	) -> Tuple[Tuple[int, int], Tuple[int, int]]:
		image = self.image.copy()
		draw = ImageDraw.Draw(image)

		font = ImageFont.truetype("gilroy.ttf", size)

		if center is None:
			x = image.width / 2
			y = image.height / 2
		else:
			x, y = center

		lines = []
		line = ""
		for word in text.split():
			if draw.textbbox((0, 0), line + word, font = font)[2] <= (constraints[0] or image.width):
				line += word + " "
			else:
				lines.append(line.strip())
				line = word + " "
		lines.append(line.strip())

		total_height = sum(draw.textbbox((0, 0), line, font = font)[3] + line_spacing for line in lines)
		y -= total_height / 2

		result = [(0, 0), (0, 0)]
		count = 0
		
		# TODO: can be optimized by first calculating and ONLY drawing if it's a good fit (and we could omit the image copy at the start...)
		for line in lines:
			line_bbox = draw.textbbox((0, 0), line, font = font)
			
			if line_bbox[3] + y >= (constraints[1] or self.image.height) or line_bbox[3] < 0:
				# NOTE: this has to be updated if the arguments get added/removed/updated/changed...
				# I didn't use named arguments so it breaks for an order change, intentional
				return self.write_text(text, center, constraints, line_spacing, size - 1, color)

			if count == 0:
				result[0] = (line_bbox[0], line_bbox[1])
			elif count == len(lines) - 1:
				result[1] = (line_bbox[2], line_bbox[3])

			x = (image.width - line_bbox[2]) // 2
			draw.text((x, y), line, font = font, fill = color)
			y += line_bbox[3] + line_spacing
			count += 1
		
		self.image = image
		return tuple(result)
		
with Image.open("background0.png") as im:
	editor = ImageEditor(im)
	
	color = (0, 255, 255)
	editor.write_text("Unveiling the Tech Giants: Shades of Good and Evil.", color = color)
	editor.write_text("1", color = color, center = editor.points.top_text, size = 75)
	editor.write_text("@gregismotion", color = color, center = editor.points.bottom_text, size = 75)

	editor.image.show()
