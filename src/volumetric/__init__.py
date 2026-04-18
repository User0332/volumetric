import importlib.metadata
from typing import Any

__version__ = importlib.metadata.version("volumetric_flask")

import os
import json
import pathlib
import dotenv
from flask import Flask

from volumetric.fs_routes import parse_fs_routes

class SecretsProxy:
	def __getattr__(self, attr: str):
		return os.environ[attr]

class PluginObjects: pass

class FSRoutesManager:
	def __init__(self, app: 'App'):
		self.app = app

	def enable(self):
		if not parse_fs_routes(self.app, "root"):
			exit(1)

class App[TPluginObjectsModel, TSecretsModel = SecretsProxy](Flask):
	def __init__(
		self,
		import_name: str,
		static_url_path: str | None = None,
		static_folder: str | os.PathLike = "static",
		static_host: str | None = None,
		host_matching: bool = False,
		subdomain_matching: bool = False,
		template_folder: str = "templates",
		instance_path: str | None = None,
		instance_relative_config: bool = False,
		root_path: str | None = None,
		secrets_path: str | None = None,
		volumetric_config: dict | None = None,
		volumetric_config_path: str = "config.json"
	):
		super().__init__(
			import_name,
			static_url_path,
			static_folder,
			static_host,
			host_matching,
			subdomain_matching,
			template_folder,
			instance_path,
			instance_relative_config,
			root_path
		)

		if secrets_path:
			dotenv.load_dotenv(pathlib.Path(self.instance_path) / secrets_path)

			self.secrets: TSecretsModel = SecretsProxy()

		self.plugin_objects: TPluginObjectsModel = PluginObjects()
		self.fs_routes = FSRoutesManager(self)

		if volumetric_config:
			self.volumetric_config = volumetric_config or {}
		elif os.path.isfile(volumetric_config_path):
			with open(volumetric_config_path, 'r') as f:
				self.volumetric_config = json.load(f)
		else:
			self.volumetric_config = {}

		self.use_local_volumetric_for_csr = self.volumetric_config.get("use_local_volumetric", False)

	def run(self, *args: Any, **kwargs: Any):
		if len(args) != 0 or len(kwargs) != 0:
			super().run(*args, **kwargs)
		else:
			super().run(**self.volumetric_config.get("run", {}))