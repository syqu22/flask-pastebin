"""
This file contains the unit tests for the user model
"""

from web.models import User


def test_user_model(session):
    """
    GIVEN a new User model
    WHEN a User is added to session
    THEN check the id is assigned correctly
    """
    user = User("Test", "test@gmail.com", "123456")

    session.add(user)
    session.commit()

    assert user.id > 0


def test_user_model_fixture(session, new_user):
    """
    GIVEN a User model
    WHEN a User is added to session
    THEN check the id is assigned correctly
    """
    session.add(new_user)
    session.commit()

    assert new_user.id > 0


def test_new_user(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check the username, email, password and Flask-Login fields are correct
    """
    assert new_user.email == "testing@user1.com"
    assert new_user.check_password("password")
    assert new_user.is_authenticated
    assert new_user.is_active
    assert new_user.check_password("password")
    assert not new_user.is_anonymous


def test_new_user_extended():
    """
    GIVEN a new User model
    WHEN a new User is created
    THEN check the username, email, password and Flask-Login fields are correct
    """
    user = User("Test", "test@gmail.com", "123456")

    assert user.username == "Test"
    assert user.email == "test@gmail.com"
    assert user.check_password("123456")
    assert user.password != "123456"


def test_user_setting_password(new_user):
    """
    GIVEN an existing User
    WHEN the password for the user is set
    THEN check the password is stored correctly and not as plaintext
    """
    new_user.set_password("password")
    assert new_user.password != "password"
    assert new_user.check_password("password")
    assert not new_user.check_password("new password")


def test_user_id(new_user):
    """
    GIVEN an existing User
    WHEN the ID of the user is defined to a value
    THEN check the user ID returns a string (and not an integer) as needed by Flask-WTF
    """
    new_user.id = 17
    assert isinstance(new_user.get_id(), str)
    assert not isinstance(new_user.get_id(), int)
    assert new_user.get_id() == "17"
