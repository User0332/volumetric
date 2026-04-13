# coding: jsx

import asyncio
from typing import Awaitable, Callable

from pyjsx import jsx, JSX


def AsyncPlaceholder(children: list[JSX], task: asyncio.Task[JSX]) -> JSX:
	if not task.done():
		return children
	
	return task.result()