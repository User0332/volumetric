
from pyjsx import JSX

def body(elem: JSX, head: JSX=""):
	return f"""<html><head>{head}</head><body>{elem}</body></html>"""