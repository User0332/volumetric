import micropip
await micropip.install('volumetric-flask')
import pyjsx.auto_setup
exec(b'from js import *\nfrom pyjsx import jsx\nfrom volumetric.csr import CSRHelpers, convert_function\n\nconsole.log("Hello, World! (from Python!)")\n\ndef btn_handler():\n\twindow.alert("Hello!")\n\ndef update():\n\tcsr = CSRHelpers()\n\n\treturn (\n\t\t<>\n\t\t\t<h1 id="heading">Hello, World!</h1>\n\t\t\t<button onclick={csr.conv_func(lambda: window.alert("Hello!"))}>Click Me!</button>\n\t\t</>\n\t)'.decode('jsx'), globals(), locals())
import volumetric
update