import pytest
from web_server.models import db, Users

from web_server import create_app


@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    yield app

    db.drop_all(app=app)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions:
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)


@pytest.fixture
def email(email):
    return email
