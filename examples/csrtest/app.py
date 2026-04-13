import os
import subprocess
from volumetric import App

app = App(__name__)

app.fs_routes.enable()

app.debug = True

project_dir = os.path.dirname(__file__)

# for local development
# subprocess.run(["poetry", "build", "-o", os.path.join(project_dir, "static/_python")], check=True)