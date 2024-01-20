from PIL import Image, ImageFilter, ImageEnhance, ImageDraw, ImageFont
import textwrap

class ImageEditor:
	def __init__(self, font_path, branding, aspect_ratio = (1, 1), blur_radius = 10, brightness = .25):
		self.font_path = font_path
		self.branding = branding
		self.aspect_ratio = aspect_ratio
		self.blur_radius = blur_radius
		self.brightness = brightness

	def crop_center(self, image):
		width, height = image.size
		new_aspect_ratio = float(self.aspect_ratio[0]) / self.aspect_ratio[1]
		if float(width) / height > new_aspect_ratio:
			new_size = (int(height * new_aspect_ratio), height)
			left = (width - new_size[0]) / 2
			top = 0
		else:
			new_size = (width, int(width / new_aspect_ratio))
			left = 0
			top = (height - new_size[1]) / 2
		right = left + new_size[0]
		bottom = top + new_size[1]
		return image.crop((int(left), int(top), int(right), int(bottom)))
	def fade(self, image):
		return ImageEnhance.Brightness(image).enhance(self.brightness)
	def blur(self, image):
		return image.filter(ImageFilter.GaussianBlur(radius=self.blur_radius))
	def write_brand(self, image):
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(self.font_path, 64)

		bbox = (image.width / 2, image.height * .875)
		text = self.branding

		draw.text(bbox, text, anchor="mm", font=font, fill=(217, 112, 74))
		return image
	def write_count(self, image, count):
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(self.font_path, 64)

		bbox = (image.width / 2, image.height * (1 - .875))

		draw.text(bbox, str(count), anchor="mm", font=font, fill=(217, 112, 74))
		return image
	def write_text(self, image, text):
		draw = ImageDraw.Draw(image)
		font = ImageFont.truetype(self.font_path, 72)

		bbox = (image.width / 2, image.height / 2)	
		text = "\n".join(textwrap.wrap(text, 30))

		draw.text(bbox, text, anchor="mm", font=font, fill=(255, 255, 255))
		return image
