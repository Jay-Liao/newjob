from flask import Flask
from flask_restplus import Api
from newjob_app.utils import file_util
from newjob_app.constants import config_constant


def init_routing():
    from newjob_app.rounting import ns

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py", silent=True)
file_util.make_dirs(app.config[config_constant.JOB_DIRECTORY])
api = Api(app, version="1.0", title="NewJob", description="A simple NewJob API")
init_routing()
