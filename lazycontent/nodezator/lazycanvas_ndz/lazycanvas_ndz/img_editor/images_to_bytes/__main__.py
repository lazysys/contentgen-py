from PIL import Image

from typing import List

def images_to_bytes(*images: type(Image)) -> [{"name": "bytes_images", "type": List[bytes]}]:
	return [image.tobytes() for image in images]

main_callable = images_to_bytes

