from typing import List

from lazycommon.entry import Entry

from io import BufferedReader

def entries_to_images(*entries: Entry) -> [{"name": "images", "type": List[BufferedReader]}]:
	return [open(entry.thumbnail, "rb") for entry in entries]

main_callable = entries_to_images
