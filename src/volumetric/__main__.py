import os
import sys
from flask import Flask
from json import load, dumps
from shutil import rmtree
from sys import argv
from importlib import import_module
from argparse import ArgumentParser

WATCH_FILES: dict[str, int] = {}

def run(force_debug: bool):
	conf = {}

	if os.path.exists("config.json"):
		with open("config.json", 'r') as f:
			conf: dict = load(f)

	sys.path.insert(0, os.getcwd()) # this is needed in case the script was run without `python -m`
	try: appmod = import_module("app")
	except ModuleNotFoundError:
		print("app.py file does not exist!")
		exit(1)
	
	try:
		app: Flask = appmod.app
	except AttributeError:
		print("app object is missing from app.py!")
		exit(1)

	if force_debug: app.debug = True
		
	app.run(**conf)

DEFAULT_ROUTE_CODE = """# coding: jsx

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
"""

DEFAULT_ROUTE_CONF = {
	"methods": ["GET"]
}

DEFAULT_CONF = {
	"host": "127.0.0.1",
	"port": 5000
}

DEFAULT_CODE = """from volumetric import App
import pyjsx.auto_setup

app = App(__name__)

app.fs_routes.enable()

app.debug = True"""

def new(name: str):
	if os.path.exists(name): rmtree(name)

	os.mkdir(name)

	os.mkdir(f"{name}/static")

	os.mkdir(f"{name}/static/js")
	open(f"{name}/static/js/index.js", 'w').write(
		"""document.getElementById("heading")
	.textContent = "Hello World!"
"""
	)

	os.mkdir(f"{name}/static/css")
	open(f"{name}/static/css/index.css", 'w').write(
		"""#heading {
	color: red;
}"""
	)

	os.mkdir(f"{name}/static/images")

	open(f"{name}/app.py", 'w').write(
		DEFAULT_CODE
	)

	open(f"{name}/config.json", 'w').write(
		dumps(DEFAULT_CONF, indent='\t')
	)

	os.mkdir(f"{name}/root")
	open(f"{name}/root/config.json", 'w').write(
		dumps(DEFAULT_ROUTE_CONF, indent='\t')
	)

	open(f"{name}/root/index.py", 'w').write(
		DEFAULT_ROUTE_CODE
	)

def route(name: str):
	if os.path.exists(name): rmtree(name)

	os.mkdir(f"{name}")
	open(f"{name}/config.json", 'w').write(
		dumps(DEFAULT_ROUTE_CONF, indent='\t')
	)

	open(f"{name}/index.py", 'w').write(
		DEFAULT_ROUTE_CODE
	)

if len(argv) < 2: argv.append('')


def main():
	parser = ArgumentParser("volumetric", description="CLI for the Volumetric Python web framework (docs: https://DOCS_SUBDOMAIN.readthedocs.io/)")
	
	subparsers = parser.add_subparsers(dest="command", required=True, help="sub-command help")

	new_parser = subparsers.add_parser(
		"new",
		help="Create a new project"
	)
	
	new_parser.add_argument(
		"name",
		help="Name to be used for the new project"
	)

	route_parser = subparsers.add_parser(
		"route",
		help="Create a new route directory"
	)

	route_parser.add_argument(
		"path",
		help="Name to be used for the new route"
	)

	run_parser = subparsers.add_parser(
		"run",
		help="Run the project"
	)

	run_parser.add_argument("--force-debug", action="store_true", help="make sure debug mode is used")

	args = parser.parse_args()

	if args.command == "route":		
		route(args.path)
	elif args.command == "new":
		new(args.name)
	else:
		run(args.force_debug)


if __name__ == "__main__":
	main()