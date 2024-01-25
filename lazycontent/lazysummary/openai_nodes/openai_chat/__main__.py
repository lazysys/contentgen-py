from ...openai import OpenAIChat

main_callable = OpenAIChat

models = OpenAIChat.models()
def _OpenAIChat(api_key: str, model: {"widget_name": "option_menu", "widget_kwargs": {"options": models}, "type": str} = models[0]) -> [{"name": "openai_chat", "type": OpenAIChat}]:
	pass

signature_callable = _OpenAIChat
