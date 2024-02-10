from lazyllm.openai import OpenAIChat, BaseOpenAILLM

main_callable = BaseOpenAILLM

models = BaseOpenAILLM.models()
def _OpenAIChat(openai_chat: OpenAIChat, model: {"widget_name": "option_menu", "widget_kwargs": { "options": models }, "type": str} = models[0]) -> [{"name": "llm", "type": BaseOpenAILLM}]:
	pass

signature_callable = _OpenAIChat
