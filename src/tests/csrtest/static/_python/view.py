import micropip
await micropip.install('volumetric-flask')
import pyjsx.auto_setup
exec(b'from js import *\nfrom pyjsx import jsx\nfrom volumetric.csr import convert_function\nfrom volumetric.xml_helpers import body\n\n\nconsole.log("Hello, World! (from Python!)")\n\ndef update():\n\treturn body(\n\t\t<>\n\t\t\t<h1 id="heading">Hello, World!</h1>\n\t\t\t<button onclick={convert_function(lambda: window.alert("Hello!"))}>Click Me!</button>\n\t\t</>\n\t)'.decode('jsx'), globals(), locals())
import volumetric
update