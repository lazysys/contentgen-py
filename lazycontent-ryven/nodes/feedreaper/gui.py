from ryven.gui_env import *

from qtpy.QtWidgets import QSpinBox
from qtpy.QtCore import Qt

class CountSpinBox(NodeInputWidget, QSpinBox):
	def __init__(self, params):
		NodeInputWidget.__init__(self, params)
		QSpinBox.__init__(self)
		
		self.setMinimum(0)

		self.valueChanged.connect(self.value_changed)

	def value_changed(self, val):
		self.update_node_input(Data(val))

	def get_state(self) -> dict:
		return {'value': self.value()}

	def set_state(self, state: dict):
		self.setValue(state['value'])


class FeedReaperNodeGui(NodeGUI):
	input_widget_classes = { 'Count': CountSpinBox }

	init_input_widgets = {
		1: {'name': 'Count', 'pos': 'besides'}
	}

export_guis([
	FeedReaperNodeGui,
])
