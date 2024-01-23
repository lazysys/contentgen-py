from ryven.gui_env import *

from qtpy.QtWidgets import QLineEdit
from qtpy.QtCore import Qt

class NodeLineEdit(NodeInputWidget, QLineEdit):
	def __init__(self, params):
		NodeInputWidget.__init__(self, params)
		QLineEdit.__init__(self)
		
		self.setPlaceholderText("Key")

		self.textChanged.connect(self.text_changed)

	def text_changed(self, val):
		self.update_node_input(Data(val))

	def get_state(self) -> dict:
		return {'text': self.text()}

	def set_state(self, state: dict):
		self.setText(state['text'])


class DotEnvVarNodeGui(NodeGUI):
	input_widget_classes = { 'Key': NodeLineEdit }

	init_input_widgets = {
		0: {'name': 'Key', 'pos': 'besides'}
	}

export_guis([
	DotEnvVarNodeGui,
])
