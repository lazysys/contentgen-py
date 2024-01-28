from ...content_type import Image as ContentImage

from PIL import Image

from typing import List

def pil_images_to_content_images(pil_images: List[type(Image)], captions: List[str]) -> [{"name": "content_images", "type": ContentImage}]:
	return [ContentImage(content = caption, image = image.tobytes()) for image, caption in zip(pil_images, captions) ]

main_callable = pil_images_to_content_images
