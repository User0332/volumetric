import os
import random
import string
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

					if (newHTML !== document.body.innerHTML) {{
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

def convert_function(ident: str, func: FunctionType) -> str:
	convd_functions[ident] = func

	return f"callconvd({ident!r})"

class IdentGenerator:
	def __init__(self, seed: int):
		self.random = random.Random(seed)
		self.seen = set()

	def _gen(self):
		return ''.join(self.random.choice(string.digits + string.ascii_letters) for _ in range(10))

	def gen(self):
		next_ident = self._gen()

		if next_ident in self.seen: return self.gen()

		self.seen.add(next_ident)
		
		return next_ident
	
class CSRHelpers:
	def __init__(self, seed: int=123456789):
		self.ident = IdentGenerator(seed)

	def conv_func(self, func: FunctionType):
		return convert_function(self.ident.gen(), func)