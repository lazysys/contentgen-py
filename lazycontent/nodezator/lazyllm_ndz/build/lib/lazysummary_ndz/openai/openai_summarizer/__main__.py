from lazysummary.openai import OpenAIChat, OpenAISummarizer

main_callable = OpenAISummarizer

def _OpenAISummarizer(api: OpenAIChat) -> [{"name": "summarizer", "type": OpenAISummarizer}]:
	pass

signature_callable = _OpenAISummarizer
