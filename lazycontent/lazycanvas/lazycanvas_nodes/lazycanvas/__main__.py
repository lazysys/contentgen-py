from ... import LazyCanvas
from ...templates import CanvasTemplate

main_callable = LazyCanvas

def _LazyCanvas(template: CanvasTemplate, branding: str) -> [{"name": "lazycanvas", "type": LazyCanvas}]:
	pass

signature_callable = _LazyCanvas
