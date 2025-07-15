# coding: jsx

from pyjsx import jsx
from flask import request
import volumetric
from volumetric.snippets.structure import Content
from volumetric.xml_helpers import body

def handler(app: volumetric.App, *args):
	
	return body(
		<Content>
			<h1 id="heading"></h1>
			<h2 id="greeting">Hello, {request.args.get("name", "noname")}!</h2>
		</Content>,
		
		head=<>
			<script src="/static/js/index.js" defer></script>
			<link rel="stylesheet" href="/static/css/index.css"/>
		</>
	)
