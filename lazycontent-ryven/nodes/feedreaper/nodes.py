from ryven.node_env import *

from lazycontent.feedreaper.feedreaper import FeedReaper, StorageConfig

guis = import_guis(__file__)

class FeedReaperStorageConfigNode(Node):
	title = 'FeedReaper Storage Config'
	tags = []
	init_inputs = [
		NodeInputType(label="Feeds file"), 
		NodeInputType(label="Used file")
	]
	init_outputs = [
		NodeOutputType(label="StorageConfig")
	]

	def update_event(self, inp=-1):
		feeds = self.input(0).payload
		used = self.input(1).payload
		
		config = StorageConfig(feeds, used)
		self.set_output_val(0, Data(config))

class FeedReaperNode(Node):
	GUI = guis.FeedReaperNodeGui

	title = 'FeedReaper'
	tags = []
	init_inputs = [
		NodeInputType(label="StorageConfig"),
		NodeInputType(label="Count")
	]
	init_outputs = [
		NodeOutputType(label="Entries")
	]

	def update_event(self, inp=-1):
		storage = self.input(0).payload
		feedreaper = FeedReaper(storage)

		count = self.input(1).payload
		
		self.set_output_val(0, Data([next(feedreaper) for _ in range(count)]))

export_nodes([
	FeedReaperStorageConfigNode,
	FeedReaperNode
])
