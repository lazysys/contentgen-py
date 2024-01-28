from typing import List

from ...entry import Entry

def entries_to_bytes_images(*entries: Entry) -> [{"name": "bytes_images", "type": List[bytes]}]:
	return [open(entry.thumbnail, "rb")]

main_callable = entries_to_bytes_images
