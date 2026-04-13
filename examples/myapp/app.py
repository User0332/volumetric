from flask import request
from volumetric import App
import pyjsx.auto_setup

app = App(__name__, secrets_path=".env")

app.fs_routes.enable()

class AuthService:
	def get_user(self) -> str | None:
		return request.args.get("user")

app.debug = True

app.plugin_objects.authservice = AuthService()