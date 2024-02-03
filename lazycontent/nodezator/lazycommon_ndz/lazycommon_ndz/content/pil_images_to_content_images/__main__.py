from lazycommon.content.types import Image as ContentImage

from PIL import Image

from io import BytesIO, BufferedReader

from typing import List

def pil_images_to_content_images(pil_images: List[type(Image)], captions: List[str]) -> [{"name": "content_images", "type": ContentImage}]:
	buffer = BytesIO()
	image.save(buffer, format="JPEG")
	buffer.seek(0)
	return [ContentImage(content = caption, image = BufferedReader(buffer)) for image, caption in zip(pil_images, captions) ]

main_callable = pil_images_to_content_images
