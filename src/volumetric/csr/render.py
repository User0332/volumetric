from functools import partial
from typing import Callable
from pyjsx import JSX

from .internal import clear_convd
from .state import ViewState
from js import document

StateClassType = ViewState

re_render_parameterless_callback: Callable[[], None] = None

def start_render(update: Callable[[StateClassType], JSX], StateClass: type[StateClassType] | None):
	global re_render_parameterless_callback

	if StateClass is None: # the attached route probably doesn't define a state class, so we just render once & signal that no state exists
		re_render(update, None)

		re_render_parameterless_callback = partial(re_render, update, None)
		return

	state = StateClass()

	re_render_parameterless_callback = partial(re_render, update, state)

	state._ViewState__attach_state_watcher(re_render_parameterless_callback)

	re_render(update, state)

def re_render(update: Callable[[StateClassType], JSX], state: StateClassType | None):
	clear_convd()

	new_html = update(state) if state is not None else update() # if the state is None, the route didn't define a state class, so don't pass any args to update()

	if new_html != document.body.innerHTML:
		document.body.innerHTML = new_html