from js import *
from pyjsx import JSX, jsx

from volumetric.csr.state import ViewState
from volumetric.csr.utils import CSRHelpers

class State(ViewState):
	number: int = 0
	name: str = "No name"

def update(state: State) -> JSX:
	csr = CSRHelpers()

	label = "hmmm"

	if state.number % 5 == 0:
		label = "Buzz"
	elif state.number % 3 == 0:
		label = "Fizz"

	return (
		<>
			<h1 id="heading"></h1>
			<button id="button" onclick={csr.conv_func(lambda: setattr(state, "number", state.number + 1))}>Increment</button>
			<p>Number: {state.number}</p>
			<p>Label: {label}</p>
			<p>Name: {state.name}</p>
		</>
	)

