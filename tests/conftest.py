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
    pastebin = Pastebin(title="test title", content="test content", syntax="text", user_id=None, expire_date=None, password=password)
    return pastebin


@pytest.fixture
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///db/{DB_NAME}"
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS "] = False
    #flask_app.config["WTF_CSRF_ENABLED"] = False

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture
def init_database(test_client):
    db.create_all()

    user1 = User("user1", "testing@user1.com", "password")
    user2 = User("user2", "testing@user2.com", "password")

    pastebin1 = Pastebin(title="test title 1", content="test content 1", syntax="text", user_id=1, expire_date=None, password=None)
    pastebin2 = Pastebin(title="test title 2", content="test content 2", syntax="css", user_id=2, expire_date=None, password="password")

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
