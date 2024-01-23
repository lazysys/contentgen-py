from lazysummary.openai import OpenAISummarizer, OpenAIChat
from lazycommon.entry import Entry
from lazycommon.content_type import *

from dotenv import load_dotenv
from attrdict import AttrDict
import os

load_dotenv()

key = os.getenv("openai_key")

api = OpenAIChat(key)
summarizer = OpenAISummarizer(api)

entry = Entry(AttrDict({"url": "www.google.com", "title": "GOOOGLE", "content": "This is da goooogle."}))

print(summarizer.summarize([entry], Microblog)) # TODO: get a proper class system for content type
