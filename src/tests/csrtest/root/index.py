from js import *
from pyjsx import jsx
from volumetric.csr import convert_function
from volumetric.xml_helpers import body


console.log("Hello, World! (from Python!)")

def update():
	return body(
		<>
			<h1 id="heading">Hello, World!</h1>
			<button onclick={convert_function(lambda: window.alert("Hello!"))}>Click Me!</button>
		</>
	)