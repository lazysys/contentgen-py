from ...feedreaper import FeedReaper
from ...lazycommon.entry import Entry

from typing import Iterator, List

def iterate_reaper(
		reaper: Iterator[Entry], 
		count: {
			"widget_name": "int_float_entry",
			"widget_kwargs": {
				"min_value": 1,
			},
			"type": int,
		} = 1
	) -> [{
		"name": "entries",
		"type": List[Entry]
	}]:
	return [next(reaper) for _ in range(count)]
	

main_callable = iterate_reaper
