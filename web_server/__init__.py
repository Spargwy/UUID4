import os

from flask import Flask, g
from flask.cli import load_dotenv
from flask_migrate import Migrate


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    try:
        os.mkdir(f"{os.curdir}/files")
    except OSError:
        pass
    load_dotenv()
    app.config['SECRET_KEY'] = os.getenv('SECRET')
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('DB_URL')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config['UPLOAD_FOLDER'] = os.path.abspath(os.curdir) + "/files"
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from web_server import aut, file_storage
    from web_server.models import db

    db.init_app(app)
    migrate = Migrate(app, db)
    app.register_blueprint(aut.bp)
    app.register_blueprint(file_storage.bp)

    app.add_url_rule("/", endpoint="index")

    return app
