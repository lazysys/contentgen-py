from lazyllm.openai import OpenAIChat, VisionOpenAILLM

main_callable = VisionOpenAILLM

models = VisionOpenAILLM.models()
def _OpenAIChat(openai_chat: OpenAIChat, model: {"widget_name": "option_menu", "widget_kwargs": { "options": models }, "type": str} = models[0]) -> [{"name": "llm", "type": VisionOpenAILLM}]:
	pass

signature_callable = _OpenAIChat
