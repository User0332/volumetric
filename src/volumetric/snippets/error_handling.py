# coding: jsx

from typing import Callable

from pyjsx import jsx, JSX


def Try(children: list[JSX], func: Callable[[], JSX], catch: Exception | tuple[Exception], fallback: JSX) -> JSX:
	try:
		return func()
	except catch:
		return fallback
