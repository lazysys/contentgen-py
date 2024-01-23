from ryven.gui_env import *

from qtpy.QtWidgets import QComboBox
from qtpy.QtCore import Qt

from lazycontent.lazycommon.content_type import *

class ContentTypeComboBox(NodeInputWidget, QComboBox):
	def __init__(self, params):
		NodeInputWidget.__init__(self, params)
		QComboBox.__init__(self)
		
		types = [Microblog, Thread, Article, Video, ShortVideo, LongVideo, Image, Carousel]

		[self.addItem(typ.__name__) for typ in types]

		self.currentTextChanged.connect(self.text_changed)

	def text_changed(self, val):
		self.update_node_input(Data(val))

	def get_state(self) -> dict:
		return {'text': self.currentText()}

	def set_state(self, state: dict):
		self.setCurrentText(state['text'])


class OpenAISummarizerNodeGui(NodeGUI):
	input_widget_classes = { 'ContentType': ContentTypeComboBox }

	init_input_widgets = {
		1: {'name': 'ContentType', 'pos': 'besides'}
	}

export_guis([
	OpenAISummarizerNodeGui,
])
