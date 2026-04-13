# coding: jsx

from flask import request
from pyjsx import jsx
import volumetric
from volumetric.snippets.conditionals import IfTruthy, NotTruthy
from volumetric.snippets.error_handling import Try
from volumetric.snippets.javascript import ClientSideRedirect
from volumetric.xml_helpers import body
from tests.myapp.annotations import User

def handler(app: volumetric.App, *args):
		
	user: User = app.plugin_objects.authservice.get_user()
	
	return body(
		<>
			<IfTruthy valid={user}>
				<h1>Hello, World!</h1>
				<h2>Secret: {app.secrets.SOME_ENV_VAR}</h2>
				<h3>Hot Reload Change Again!</h3>
				<Try func={lambda: <h1>{some_unknown_name}</h1>} catch={Exception} fallback={<div>error!</div>}/>
			</IfTruthy>
			<NotTruthy valid={user}>
				<ClientSideRedirect to="/"/>
			</NotTruthy>
		</>
	)
