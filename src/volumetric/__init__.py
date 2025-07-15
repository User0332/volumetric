import os
import typing as t
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

class App(Flask):
	def __init__(
		self,
		import_name: str,
		static_url_path: t.Optional[str] = None,
		static_folder: t.Optional[t.Union[str, os.PathLike]] = "static",
		static_host: t.Optional[str] = None,
		host_matching: bool = False,
		subdomain_matching: bool = False,
		template_folder: t.Optional[str] = "templates",
		instance_path: t.Optional[str] = None,
		instance_relative_config: bool = False,
		root_path: t.Optional[str] = None,
		secrets_path: t.Optional[str] = None
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
			dotenv.load_dotenv(f"{self.instance_path}/{secrets_path}")
			
			self.secrets = SecretsProxy()

		self.plugin_objects = PluginObjects()
		self.fs_routes = FSRoutesManager(self)