from ryven.node_env import *

from lazysummary.openai import OpenAISummarizer, OpenAIChat

guis = import_guis(__file__)

class OpenAIChatNode(Node):
	title = 'OpenAI Chat API'
	tags = []
	init_inputs = [NodeInputType(label="OpenAI API key")]
	init_outputs = [NodeOutputType(label="OpenAI Chat API")]

	def update_event(self, inp=-1):
		self.set_output_val(0, Data(OpenAIChat(self.input(0).payload)))

class OpenAISummarizerNode(Node):
	GUI = guis.OpenAISummarizerNodeGui

	title = 'OpenAI Summarizer'
	tags = []
	init_inputs = [
		NodeInputType(label="OpenAI Chat API"),
		NodeInputType(label="Content type"),
		NodeInputType(label="Entries")
	]
	init_outputs = [NodeOutputType(label="Summary")]

	def update_event(self, inp=-1):
		api = OpenAISummarizer(self.input(0).payload)

		typ = self.input(1).payload
		entries = self.input(2).payload
		
		summary = api.summarize(entries, typ)

		self.set_output_val(0, Data(summary))

export_nodes([
	OpenAIChatNode,
	OpenAISummarizerNode
])
