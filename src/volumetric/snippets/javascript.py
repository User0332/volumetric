# coding: jsx

from pyjsx import jsx, JSX

def ClientSideRedirect(children: list[JSX], to: str):
	return <script>location.href = {repr(to)}</script>