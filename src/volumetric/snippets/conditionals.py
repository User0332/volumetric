# coding: jsx

from typing import Any, Callable

from pyjsx import jsx, JSX


def IfTruthy(children: list[JSX], valid: Any | None, action: Callable[[], None]=lambda: None) -> JSX:
	if valid:
		action()
		return children

	return ""

def NotTruthy(children: list[JSX], valid: Any | None, action: Callable[[], None]=lambda: None) -> JSX:
	if not valid:
		action()
		return children

	return ""