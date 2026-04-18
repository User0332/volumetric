import os
import subprocess
import sys
from json import dumps
from shutil import rmtree
from importlib import import_module
from argparse import ArgumentParser
from .import App, __version__ as VOLMETRIC_VERSION

WATCH_FILES: dict[str, int] = {}

def run(force_debug: bool):
	if not os.path.isfile(f"app.py"):
		print("app.py file does not exist!")
		exit(1)

	sys.path.insert(0, os.getcwd()) # this is needed in case the script was run without `python -m`

	appmod = import_module("app")

	try:
		app: App = appmod.app
	except AttributeError:
		print("app object is missing from app.py!")
		exit(1)

	if force_debug: app.debug = True

	app.run()

DEFAULT_SSR_ROUTE_CODE = """# coding: jsx

from pyjsx import jsx
import volumetric
from volumetric.xml_helpers import body

def handler(app: volumetric.App, *args):	
	return body(
		<>
			<h1 id="heading"></h1>
		</>,
		head=<>
			<script src="/static/js/index.js" defer></script>
			<link rel="stylesheet" href="/static/css/index.css"/>
		</>
	)
"""

DEFAULT_CSR_ROUTE_CODE = """from js import *
from pyjsx import jsx

def update():
	return (
		<>
			<h1 id="heading"></h1>
		</>
	)

"""

DEFAULT_SSR_ROUTE_CONF = {
	"methods": ["GET"]
}

DEFAULT_CSR_ROUTE_CONF = {
	"methods": ["GET"],
	"csr": True
}

DEFAULT_SSR_CONF = {
	"run": {
		"host": "127.0.0.1",
		"port": 5000
	}
}

DEFAULT_CSR_CONF = {
	"run": {
		"host": "127.0.0.1",
		"port": 5000
	},
	"use_local_volumetric": False
}

DEFAULT_CODE = """from volumetric import App

app = App(__name__)

app.fs_routes.enable()

app.debug = True"""

def new(name: str, csr: bool):
	if os.path.exists(name): rmtree(name)

	os.mkdir(name)

	os.mkdir(f"{name}/static")

	os.mkdir(f"{name}/static/js")
	if not csr: open(f"{name}/static/js/index.js", 'w').write(
		"""document.getElementById("heading")
	.textContent = "Hello World!"
"""
	)

	os.mkdir(f"{name}/static/css")
	if not csr: open(f"{name}/static/css/index.css", 'w').write(
		"""#heading {
	color: red;
}"""
	)

	os.mkdir(f"{name}/static/images")

	open(f"{name}/app.py", 'w').write(
		DEFAULT_CODE
	)

	os.mkdir(f"{name}/root")

	if csr:
		open(f"{name}/config.json", 'w').write(
			dumps(DEFAULT_CSR_CONF, indent='\t')
		)

		open(f"{name}/root/config.json", 'w').write(
			dumps(DEFAULT_CSR_ROUTE_CONF, indent='\t')
		)

		open(f"{name}/root/index.py", 'w').write(
			DEFAULT_CSR_ROUTE_CODE
		)

		os.mkdir(f"{name}/static/_python")
	else:
		open(f"{name}/config.json", 'w').write(
			dumps(DEFAULT_SSR_CONF, indent='\t')
		)

		open(f"{name}/root/config.json", 'w').write(
			dumps(DEFAULT_SSR_ROUTE_CONF, indent='\t')
		)

		open(f"{name}/root/index.py", 'w').write(
			DEFAULT_SSR_ROUTE_CODE
		)

def route(path: str, csr: bool):
	if not os.path.isdir("root"):
		print("volumetric route must be called from the app directory!")
		exit(1)

	if not path.startswith('/'):
		print("pathname must start from root path! (/)")
		exit(1)

	route_path = f"root{path}"

	if os.path.exists(route_path): rmtree(route_path)

	os.makedirs(route_path)

	if csr:
		open(f"{route_path}/config.json", 'w').write(
			dumps(DEFAULT_CSR_ROUTE_CONF, indent='\t')
		)

		open(f"{route_path}/index.py", 'w').write(
			DEFAULT_CSR_ROUTE_CODE
		)
	else:
		open(f"{route_path}/config.json", 'w').write(
			dumps(DEFAULT_SSR_ROUTE_CONF, indent='\t')
		)

		open(f"{route_path}/index.py", 'w').write(
			DEFAULT_SSR_ROUTE_CODE
		)

def downloadwhl():
	subprocess.run([sys.executable, "-m", "pip", "download", f"volumetric-flask=={VOLMETRIC_VERSION}", "--no-deps", "-d", "static/_python"], check=True)
	print("Downloaded volumetric wheel to static/_python/")

def main():
	parser = ArgumentParser("volumetric", description="CLI for the Volumetric Python web framework")

	subparsers = parser.add_subparsers(dest="command", required=True, help="sub-command help")

	new_parser = subparsers.add_parser(
		"new",
		help="Create a new project"
	)

	new_parser.add_argument(
		"name",
		help="Name to be used for the new project"
	)

	new_parser.add_argument(
		"--csr",
		help="Generate the project with Volumetric CSR support",
		action="store_true"
	)

	route_parser = subparsers.add_parser(
		"route",
		help="Create a new route directory"
	)

	route_parser.add_argument(
		"path",
		help="Name to be used for the new route"
	)

	route_parser.add_argument(
		"--csr",
		help="Make this route client-side rendered",
		action="store_true"
	)

	run_parser = subparsers.add_parser(
		"run",
		help="Run the project"
	)

	run_parser.add_argument("--force-debug", action="store_true", help="make sure debug mode is used")

	downloadwhl_parser = subparsers.add_parser(
		"downloadwhl",
		help="Download the current version volumetric wheel via pip and place it in _python/ for use_local_volumetric CSR mode"
	)

	args = parser.parse_args()

	if (not os.path.isfile("app.py") or not os.path.isfile("config.json")) and args.command != "new":
		print("app.py or config.json not found! Make sure to run this command from the root of your Volumetric project.")
		exit(1)

	if args.command == "route":
		route(args.path, args.csr)
	elif args.command == "new":
		new(args.name, args.csr)
	elif args.command == "downloadwhl":
		downloadwhl()
	elif args.command == "run":
		run(args.force_debug)

if __name__ == "__main__":
	main()