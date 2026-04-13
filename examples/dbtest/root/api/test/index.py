# coding: jsx

from pyjsx import jsx
import volumetric
from volumetric.xml_helpers import body

def handler(app: volumetric.App, *args):	
	return body(
		<h1 id="heading"></h1>,
		head=<>
			<script src="/static/js/index.js" defer></script>
			<link rel="stylesheet" href="/static/css/index.css"/>
		</>
	)
