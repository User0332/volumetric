import asyncio
import json
from typing import Awaitable, Callable
from pyodide import __version__ as PYODIDE_VERSION
from .. import __version__ as VOLMETRIC_VERSION


def route_to_view(code: str, route: str, use_local_volumetric: bool) -> Callable[[], str]:
	volumetric_package = f"/static/_python/volumetric_flask-{VOLMETRIC_VERSION}-py3-none-any.whl" if use_local_volumetric else f"volumetric-flask=={VOLMETRIC_VERSION}"

	frontend_header = f"""import micropip
await micropip.install({volumetric_package!r})
import pyjsx.auto_setup
"""

	code_wrapped = f"exec({code.encode()!r}.decode('jsx'), globals(), locals())\n"

	frontend_footer = """import volumetric
import volumetric.csr.state
import volumetric.csr.render
volumetric.csr.render.start_render(update, volumetric.csr.state.STATE_CLASS)"""

	frontend_code = frontend_header+code_wrapped+frontend_footer

	js_safe_python_code = json.dumps(frontend_code)

	frontend_html = f"""<!DOCTYPE html>
<html>
	<head>
		<script src="https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js"></script>
		<script>
			const pyodidePromise = loadPyodide();

			let update = null;
			let state = null;

			async function main() {{
				const pyodide = await pyodidePromise;
				
				await pyodide.loadPackage("micropip")

				const returnValue = await pyodide.runPythonAsync({js_safe_python_code});
			}}

			async function callconvd(name) {{
				const pyodide = await pyodidePromise;
			
				const volumetric = pyodide.pyimport("volumetric");
				
				volumetric.csr.internal.convd_functions.get(name)();
			}}

			main();
		</script>
	</head>
	<body></body>
</html>"""

	fn = lambda: frontend_html
	fn.__name__ = f"csr_view_{route.strip('/').replace('/', '_')}"

	return fn

convd_functions = {}

def clear_convd():
	convd_functions.clear()

def convert_function(ident: str, func: Callable) -> str:
	convd_functions[ident] = func

	return f"callconvd({ident!r})"

# list of (function, args, kwargs, Task)
# we can't use a dict because arg types could be unhashable, so we'll use __eq__ checks instead
async_jobs: list[tuple[Callable, tuple, dict, asyncio.Task]] = []

def find_job[T](func: Callable[..., Awaitable[T]], args: tuple, kwargs: dict[str]) -> asyncio.Task[T] | None:
	for func, args, kwargs, task in async_jobs:
		if func == func and args == args and kwargs == kwargs:
			return task

	return None

def dispatch_job[T](func: Callable[..., Awaitable[T]], args: tuple, kwargs: dict[str]) -> asyncio.Task[T]:
	job = asyncio.create_task(func(*args, **kwargs))

	async_jobs.append((func, args, kwargs, job))

	return job