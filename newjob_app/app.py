from flask import Flask
from flask import Blueprint
from flask import render_template
from flask_restplus import Api
from newjob_app.utils import file_util
from newjob_app import setting


def init_routing():
    from newjob_app.rounting import ns


# Build flask app
app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py", silent=True)
file_util.make_dirs(setting.JOB_DIRECTORY)

# Setup routing
bp = Blueprint("api", __name__)
api = Api(bp, version="1.0", title="NewJob", description="A simple NewJob API")
init_routing()
app.register_blueprint(bp, url_prefix="/newjob")


@app.route("/apidoc")
def apidoc():
    return render_template("swagger_ui.html")
