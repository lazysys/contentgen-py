from ... import LazyCanvas

from PIL import Image

from typing import List

def blocks_to_images(lazycanvas: LazyCanvas, blocks: List[str]) -> [{"name": "images", "type": List[type(Image)]}]:
	master = blocks[0]
	slides = blocks[1:]
	return [lazycanvas.master_slide(master)] + [lazycanvas.carousel_slide(slide, i) for i, slide in enumerate(slides)]

main_callable = blocks_to_images
