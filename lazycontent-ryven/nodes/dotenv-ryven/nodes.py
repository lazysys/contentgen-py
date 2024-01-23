from ryven.node_env import *

from dotenv import load_dotenv
import os

guis = import_guis(__file__)

class DotEnvVarNode(Node):
	GUI = guis.DotEnvVarNodeGui

	title = 'DotEnv variable'
	tags = []
	init_inputs = [NodeInputType(label="Key")]
	init_outputs = [NodeOutputType(label="Value")]
	
	def __init__(self, params):
		super().__init__(params)
		load_dotenv()

	def update_event(self, inp=-1):
		key = self.input(0).payload
		value = os.getenv(key)			

		self.set_output_val(0, Data(value))

export_nodes([
	DotEnvVarNode,
])
