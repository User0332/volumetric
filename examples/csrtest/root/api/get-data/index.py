# coding: jsx

from flask import jsonify
from pyjsx import jsx
import volumetric
from volumetric.xml_helpers import body

def handler(app: volumetric.App, *args):	
	return jsonify({
		"data": {
			"key": "some structured data",
			"num": 12
		}
	})