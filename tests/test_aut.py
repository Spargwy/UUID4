import pytest
from flask import session, g

from web_server.models import Users


def test_register(client, app):
    assert client.get("/register").status_code == 200

    response = client.post("/register", data={"username": "a",
                                              "email": "example@mail.com",
                                              "password": "a"})
    assert "http://localhost/login" == response.headers["Location"]

    with app.app_context():
        assert (
            Users.query.filter_by(username='a').first() is not None
        )


@pytest.mark.parametrize(
    ("username", "email", "password", "message"),
    (
            ("", "", "", b"Username is required."),
            ("a", "", "", b"Email is required"),
            ("a", "a", "", b"Password is required"),
            ("test", "test", "test", b"already registered"),
    ),
)
def test_register_validate_input(client, username, email, password, message):
    response = client.post(
        "/register", data={"username": username, "email": email, "password": password}
    )
    assert message in response.data


def test_login(client, auth):
    assert client.get("/login").status_code == 200

    response = auth.login()
    assert response.headers["Location"] == "http://localhost/"

    with client:
        client.get("/")
        assert session["user_id"] == 1
        assert g.user.username == "test"


@pytest.mark.parametrize(
    ("username", "password", "message"),
    (("a", "test", b"Incorrect username"), ("test", "a", b"Incorrect password")),
)
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    assert message in response.data


def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert "user_id" not in session
