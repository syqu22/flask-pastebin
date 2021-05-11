import pytest

from web.models import User, Pastebin
from web import create_app, db

DB_NAME = "test_database.db"

@pytest.fixture
def new_user():
    password = "password"
    user = User("user1", "testing@user1.com", password)
    return user

@pytest.fixture
def new_pastebin():
    password = "password"
    pastebin = Pastebin("test title", "test content", "text", None, None, password)
    return pastebin


@pytest.fixture
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db/{DB_NAME}"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture
def init_database(test_client):
    db.create_all()

    user1 = User("user1", "testing@user1.com", "password")
    user2 = User("user2", "testing@user2.com", "password")

    pastebin1 = Pastebin("test title 1", "test content 1", "text", None, None, None)
    pastebin2 = Pastebin("test title 2", "test content 2", "css", 1, None, "password")

    db.session.add(user1)
    db.session.add(user2)
    db.session.add(pastebin1)
    db.session.add(pastebin2)

    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture
def login_default_user(test_client):
    test_client.post("/login", data=dict(username="user1", password="password"), follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)
