import asyncio
from js import *
from pyjsx import jsx
from volumetric.csr.utils import CSRHelpers, include_css
from volumetric.snippets.csr import AsyncPlaceholder

include_css("index.css")

console.log("Hello, World! (from Python!)")

async def get_data():
	resp = await window.fetch("/api/get-data")
	return (await resp.json()).to_py()

async def render_data():
	data = await get_data()

	await asyncio.sleep(2) # artificial delay

	return (
		<>
			<h1>Data: {data["data"]}</h1>
		</>
	)

def update():
	csr = CSRHelpers()

	data_renderer = csr.dispatch(render_data)

	return (
		<>
			<h1 id="heading">Hello, World!</h1>
			<button onclick={csr.conv_func(lambda: window.alert("Hello!"))}>Click Me!</button>
			<AsyncPlaceholder task={data_renderer}>
				<div>Loading data from API...</div>
			</AsyncPlaceholder>
		</>
	)