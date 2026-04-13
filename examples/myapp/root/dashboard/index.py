# coding: jsx

from pyjsx import jsx
import volumetric
from volumetric.snippets.structure import Content
from volumetric.xml_helpers import body

def handler(app: volumetric.App, *args):	
	return body(
		<Content>
			<h1>Hello, World!</h1>
		</Content>
	)