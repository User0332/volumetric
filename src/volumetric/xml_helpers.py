
import html
from typing import Any
from pyjsx import JSX

def body(elem: JSX, head: JSX=""):
	return f"""<html><head>{head}</head><body>{elem}</body></html>"""

def escape_repr(obj: Any):
	return html.escape(repr(obj), quote=True)