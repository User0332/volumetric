import asyncio
from math import e
import os
import pathlib
from pydoc import doc
import random
import string
from types import FunctionType
from typing import Awaitable, Callable, Literal

from .internal import convert_function, dispatch_job, find_job
from . import render as internal_render

from js import document


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

	def dispatch[T](self, func: Callable[..., Awaitable[T]], re_render_on_completion: bool=True, *args, **kwargs) -> asyncio.Task[T]:
		if (dispatched_job := find_job(func, args, kwargs)) is not None:
			return dispatched_job

		task = dispatch_job(func, args, kwargs)

		if re_render_on_completion:
			task.add_done_callback(lambda _: internal_render.re_render_parameterless_callback())

		return task

ResourceType = Literal["js", "css", "infer"]

def include(resource: str, rtype: ResourceType="infer", asset_base_path: str="/static"):
	if rtype == "infer":
		if resource.endswith(".js"):
			rtype = "js"
		elif resource.endswith(".css"):
			rtype = "css"
		else:
			raise ValueError(f"Could not infer resource type for {resource}.")

	if rtype == "js":
		elem = document.createElement("script")
		elem.src = (pathlib.Path(asset_base_path) / resource).as_posix()

		document.head.appendChild(elem)
	elif rtype == "css":
		elem = document.createElement("link")
		elem.rel = "stylesheet"
		elem.href = (pathlib.Path(asset_base_path) / resource).as_posix()

		document.head.appendChild(elem)
	else:
		raise ValueError(f"Invalid resource type: {rtype}. Must be 'js', 'css', or 'infer'.")

def include_css(resource: str, css_base_path: str="/static/css"):
	return include(resource, rtype="css", asset_base_path=css_base_path)

def include_js(resource: str, js_base_path: str="/static/js"):
	return include(resource, rtype="js", asset_base_path=js_base_path)