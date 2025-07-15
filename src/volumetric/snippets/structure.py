# coding: jsx

from typing import Callable
from pyjsx import jsx, JSX

def Content(children: list[JSX], **props):
	props["class"] = ("content "+props.get("class", "")).strip()
	
	return <div {...props}>{children}</div>