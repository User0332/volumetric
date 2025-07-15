from functools import partial
from importlib import import_module
import os
import json
import sys
from types import FunctionType
from flask import Flask

def appbind(func: FunctionType, app: Flask, name: str):
	new = partial(func, app)
	new.__name__ = name

	return new

def modularize_index(path: str):
	dirname = os.path.dirname(path)

	sys.path.insert(0, dirname)

	mod = import_module("index")

	sys.path.remove(dirname)

	return mod
	

def parse_fs_routes(app: Flask, rootdir: str, parent: str='/') -> bool:
	conf = f"{rootdir}/config.json"
	index_fname = f"{rootdir}/index.py"
	
	if os.path.exists(conf):
		with open(conf, 'r') as f:
			try: config: dict = json.load(f)
			except json.decoder.JSONDecodeError:
				print(f"{conf} is invaliZd!")
				return False
	else: config = {}

	if os.path.exists(index_fname):
		try:
			index = modularize_index(index_fname)
		except Exception as e:
			print(f"{index_fname} threw an error!\n{e}")
			return False

		if not hasattr(index, "handler"):
			print(f"{index_fname} is missing a handler function!")
			return False

		handler = appbind(
			index.handler,
			app,
			f"{parent}_handler"
		)

		app.route(parent, **config)(handler)

		del sys.modules["index"]

	for subdir in os.listdir(rootdir):
		sub_qual = f"{rootdir}/{subdir}"
		if os.path.isdir(sub_qual):
			if not parse_fs_routes(app, sub_qual, f"{parent}{subdir}/"):
				return False

	return True

