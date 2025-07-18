from js import *
from pyjsx import jsx
from volumetric.csr import CSRHelpers, convert_function

console.log("Hello, World! (from Python!)")

def btn_handler():
	window.alert("Hello!")

def update():
	csr = CSRHelpers()

	return (
		<>
			<h1 id="heading">Hello, World!</h1>
			<button onclick={csr.conv_func(lambda: window.alert("Hello!"))}>Click Me!</button>
		</>
	)