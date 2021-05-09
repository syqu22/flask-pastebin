import pytest

from web import create_app, db
from web.models.user import User
from web.models.pastebin import Pastebin

@pytest.fixture(scope="module")
def new_user():
    password = "password"
    user = User("testing user", "testing@user.com", password)
    return user

@pytest.fixture(scope="module")
def new_pastebin():
    password = "password"
    pastebin = Pastebin("test content", "text", None, "test title", None, password)
    return pastebin


@pytest.fixture(scope="module")
def test_client():
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client

@pytest.fixture(scope="module")
def init_database(client):
    db.create_all()

    user1 = User("testing user 1", "testing@user1.com", "password")
    user2 = User("testing user 2", "testing@user2.com", "password")
    
    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()

    pastebin1 = Pastebin("Test content pastebin 1", "text", user1.id)
    pastebin2 = Pastebin("Test content pastebin 2", "css", None)

    db.session.add(pastebin1)
    db.session.add(pastebin2)
    db.session.commit()

    yield

    db.drop_all()

@pytest.fixture(scope="function")
def login_default_user(test_client):
    test_client.post("/login",data=dict("testing user", "testing@user", "password"), follow_redirects=True)

    yield

    test_client.get('/logout', follow_redirects=True)
