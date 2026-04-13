from volumetric import App
from db import db
import pyjsx.auto_setup

app = App(__name__)

app.fs_routes.enable()

app.debug = True


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"

db.init_app(app)