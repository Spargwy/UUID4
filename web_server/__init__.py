import os

from flask import Flask
from flask.cli import load_dotenv
from flask_migrate import Migrate

from web_server.models import Users


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
        from web_server.models import db
        app.config.from_mapping(test_config)
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv('TEST_DB_URL')
        db.init_app(app)
        with app.app_context():
            db.create_all()
            user = Users("test", "test",
                         'pbkdf2:sha256:50000$TCI4GzcX$0de171a4f4dac32e3364c7ddc7c14f3e2fa61f2d17574483f7ffbb431b4acb2f')
            db.session.add(user)
            db.session.commit()
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
