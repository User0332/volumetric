from volumetric import App

app = App(__name__)

app.fs_routes.enable()

app.debug = True