from dataclasses import dataclass
from typing import List, Type, TypeVar, Generic

class TypeNotImplemented(Exception):
	def __init__(self, runner: Any, name: str):
		super().__init__(f"Type {name} is not implemented by the {type(runner).__name__} runner!")
class TypeDisabled(Exception):
	def __init__(self, runner: Any, name: str):
		super().__init__(f"Type {name} is disabled on {type(runner).__name__} runner!")

T = TypeVar("T")
R = TypeVar("R")
@dataclass
class Runner(Generic[T, R]):
	types: List[Type[Content]]

	def __getattr__(self, name: str):
		raise TypeNotImplemented(self, name)
	
	def _is_type_in(self, typ: Type[T], target_list: List) -> bool:
		target_list = [target.__name__ for target in target_list]
		return any([mro.__name__ in target_list for mro in typ.mro()])
	def _is_type_enabled(self, typ: Type[T]) -> bool:
		return self._is_type_in(typ, self.types)
	def _can_run(self, typ: Type[T]) -> bool:
		return True if len(types) <= 0 else self._is_type_enabled(typ)

	def run(self, typ: Type[T], *params) -> R:
		if self._can_run(typ):
			while True:
				mro = typ.mro()
				try:
					return getattr(self, typ.__name__)(*params)
				except TypeNotSupported:
					typ = mro[1]
				if len(mro) <= 2:
					raise TypeNotSupported(typ.__name__)
		else:
			raise TypeDisabled(self, typ.__name__)
