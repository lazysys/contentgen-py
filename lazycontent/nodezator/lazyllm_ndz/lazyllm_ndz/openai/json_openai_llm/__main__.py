from lazyllm.openai import OpenAIChat, JSONOpenAILLM

main_callable = JSONOpenAILLM

models = JSONOpenAILLM.models()
def _OpenAIChat(openai_chat: OpenAIChat, model: {"widget_name": "option_menu", "widget_kwargs": { "options": models }, "type": str} = models[0]) -> [{"name": "llm", "type": JSONOpenAILLM}]:
	pass

signature_callable = _OpenAIChat
