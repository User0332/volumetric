import os
from types import FunctionType

from .constants import PYODIDE_VERSION

def route_to_view(code: str, route: str) -> FunctionType:
	frontend_header = """import micropip
await micropip.install('volumetric-flask')
import pyjsx.auto_setup
"""

	code_wrapped = f"exec({code.encode()!r}.decode('jsx'), globals(), locals())\n"

	frontend_footer = "import volumetric\nupdate" # return value to JS

	frontend_code = frontend_header+code_wrapped+frontend_footer

	py_residence_dir = f"static/_python{route}"

	if not os.path.exists(py_residence_dir):
		os.makedirs(py_residence_dir)

	py_residence = os.path.join(py_residence_dir, "view.py")

	open(py_residence, 'w').write(frontend_code)

	# TODO: optimize DOM updates

	frontend_html = f"""<!DOCTYPE html>
<html>
	<head>
		<script src="https://cdn.jsdelivr.net/pyodide/v{PYODIDE_VERSION}/full/pyodide.js"></script>
		<script>
			const pyodidePromise = loadPyodide();

			async function main() {{
				const pyodide = await pyodidePromise;
				
				await pyodide.loadPackage("micropip")

				const resource = await fetch("/{py_residence}");
				const code = await resource.text();
				const update = await pyodide.runPythonAsync(code);

				console.log("volumetric: starting render");

				document.body.innerHTML = update();

				const renderWorker = new Worker("/static/js/render-worker.js", {{ type: "module" }});

				renderWorker.onmessage = (ev) => {{
					if (ev.data === "ready") {{
						renderWorker.postMessage({{ type: "start" }});
						return;
					}}

					console.log("volumetric: new render");

					const {{ newHTML }} = ev.data;

					if (newHTML != document.body.innerHTML) {{
						document.body.innerHTML = newHTML;
					}}
				}};

				renderWorker.onerror = function(error) {{
					console.error('Worker error:', error);
				}};

				
				console.log("volumetric: worker ready");

				renderWorker.postMessage({{
					type: "init",
					code
				}});

				console.log("volumetric: worker message posted");
			}}

			async function callconvd(name) {{
				const pyodide = await pyodidePromise;
			
				const volumetric = pyodide.pyimport("volumetric");
				
				volumetric.csr.convd_functions.get(name)();
			}}

			main();
		</script>
	</head>
	<body></body>
</html>"""
	
	return lambda: frontend_html

convd_functions = {}

def clear_convd():
	convd_functions.clear()

def convert_function(func: FunctionType) -> str:
	convd_functions[repr(func)] = func

	return f"callconvd({repr(func)!r})"