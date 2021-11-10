from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    hashed_password = db.Column(db.String(128))

    def __init__(self, username, email, hashed_password):
        self.hashed_password = hashed_password
        self.username = username
        self.email = email


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, index=True)
    name = db.Column(db.String, unique=True, index=True)
    source_name = db.Column(db.String)
    accessibility = db.Column(db.String)

    def __init__(self, user_id, name, source_name, accessibility):
        self.user_id = user_id
        self.name = name
        self.source_name = source_name
        self.accessibility = accessibility
