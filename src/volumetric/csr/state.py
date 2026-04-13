from typing import Callable

from ..exceptions import MultipleStateClassException

STATE_CLASS: type['ViewState'] = None
RERENDER_REQUIRED = False # yeah a single boolean global to handle this isn't great but it works for now

class StateWatcherProxy:
	def __init__(self, obj: object, on_state_changed: Callable[[], None]):
		self.__obj = obj
		self.__on_state_changed = on_state_changed

	def __iadd__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj += other
		self.__on_state_changed()

		return self

	def __isub__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj -= other
		self.__on_state_changed()

		return self

	def __imul__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj *= other
		self.__on_state_changed()

		return self

	def __itruediv__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj /= other
		self.__on_state_changed()

		return self

	def __ifloordiv__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj //= other
		self.__on_state_changed()

		return self

	def __imod__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj %= other
		self.__on_state_changed()

		return self

	def __ipow__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj **= other
		self.__on_state_changed()

		return self

	def __iand__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj &= other
		self.__on_state_changed()

		return self

	def __ior__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj |= other
		self.__on_state_changed()

		return self

	def __ixor__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj ^= other
		self.__on_state_changed()

		return self

	def __ilshift__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj <<= other
		self.__on_state_changed()

		return self

	def __irshift__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj >>= other
		self.__on_state_changed()

		return self

	def __imatmul__(self, other: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj @= other
		self.__on_state_changed()

		return self

	def __setitem__(self, key: object, value: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		obj[key] = value
		self.__on_state_changed()

	def __delitem__(self, key: object):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		del obj[key]
		self.__on_state_changed()

	def __delattr__(self, name: str):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		delattr(obj, name)
		self.__on_state_changed()

	# String representations
	def __str__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return str(obj)

	def __repr__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return repr(obj)

	def __format__(self, format_spec: str):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return format(obj, format_spec)

	# Comparison operators
	def __eq__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj == other

	def __ne__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj != other

	def __lt__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj < other

	def __le__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj <= other

	def __gt__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj > other

	def __ge__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj >= other

	# Hashing and boolean conversion
	def __hash__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return hash(obj)

	def __bool__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return bool(obj)

	# Type conversions
	def __bytes__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return bytes(obj)

	def __int__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return int(obj)

	def __float__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return float(obj)

	def __complex__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return complex(obj)

	# Container protocol
	def __len__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return len(obj)

	def __length_hint__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj.__length_hint__()

	def __getitem__(self, key):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return StateWatcherProxy(obj[key])

	def __contains__(self, item):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return item in obj

	def __iter__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return iter(obj)

	def __reversed__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return reversed(obj)

	# Unary operators
	def __neg__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return -obj

	def __pos__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return +obj

	def __abs__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return abs(obj)

	def __invert__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return ~obj

	# Binary operators (non-augmented)
	def __add__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj + other

	def __sub__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj - other

	def __mul__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj * other

	def __truediv__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj / other

	def __floordiv__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj // other

	def __mod__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj % other

	def __pow__(self, other, modulo=None):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		if modulo is None:
			return obj ** other
		return pow(obj, other, modulo)

	def __lshift__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj << other

	def __rshift__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj >> other

	def __and__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj & other

	def __or__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj | other

	def __xor__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj ^ other

	def __matmul__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj @ other

	# Reflected binary operators
	def __radd__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other + obj

	def __rsub__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other - obj

	def __rmul__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other * obj

	def __rtruediv__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other / obj

	def __rfloordiv__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other // obj

	def __rmod__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other % obj

	def __rpow__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other ** obj

	def __rlshift__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other << obj

	def __rrshift__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other >> obj

	def __rand__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other & obj

	def __ror__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other | obj

	def __rxor__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other ^ obj

	def __rmatmul__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return other @ obj

	# Other operations
	def __divmod__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return divmod(obj, other)

	def __rdivmod__(self, other):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return divmod(other, obj)

	def __index__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj.__index__()

	def __round__(self, n=None):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return round(obj, n)

	def __trunc__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		import math
		return math.trunc(obj)

	def __floor__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		import math
		return math.floor(obj)

	def __ceil__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		import math
		return math.ceil(obj)

	# Context manager
	def __enter__(self):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj.__enter__()

	def __exit__(self, exc_type, exc_val, exc_tb):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj.__exit__(exc_type, exc_val, exc_tb)

	# Callable
	def __call__(self, *args, **kwargs):
		obj = super().__getattribute__("_StateWatcherProxy__obj")
		return obj(*args, **kwargs)

	# Attribute access (delegate to wrapped object)
	def __getattribute__(self, name: str):
		if name.startswith("_StateWatcherProxy__"):
			return super().__getattribute__(name)

		return StateWatcherProxy(
			super().__getattribute__("_StateWatcherProxy__obj").__getattribute__(name),
			self.__on_state_changed
		)

	def __setattr__(self, name: str, value):
		if name.startswith("_StateWatcherProxy__"):
			return super().__setattr__(name, value)

		super().__getattribute__("_StateWatcherProxy__obj").__setattr__(name, value)

		self.__on_state_changed()


class ViewState:
	def __attach_state_watcher(self, on_state_changed: Callable[[], None]):
		self.__on_state_changed = on_state_changed

	def __init_subclass__(cls):
		super().__init_subclass__()

		# we might allow multiple state classes later for different components but for now we only want one per view
		global STATE_CLASS

		if STATE_CLASS is not None:
			raise MultipleStateClassException("Each view may only have one state class")

		STATE_CLASS = cls

	def __getattribute__(self, name: str):
		if name.startswith("_ViewState__"):
			return super().__getattribute__(name)

		return StateWatcherProxy(super().__getattribute__(name), self.__on_state_changed)

	def __setattr__(self, name: str, value):
		if name.startswith("_ViewState__"):
			super().__setattr__(name, value)
			return

		super().__setattr__(name, value)

		self.__on_state_changed()

	def __delattr__(self, name: str):
		if name.startswith("_ViewState__"):
			super().__delattr__(name)
			return

		super().__delattr__(name)

		self.__on_state_changed()