"""
This file contains the unit tests for the user model
"""
from web.models.user import User


def test_new_user():
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that username, email, password and Flask-Login fields are correct
    """
    password = "password"
    user = User("test user", "testing@user.com", password)

    assert user.email == "testing@user.com"
    assert user.check_password(password)
    assert user.is_authenticated
    assert user.is_active
    assert user.is_valid("password", "password")
    assert not user.is_anonymous

def test_new_user_with_fixture(new_user):
    """
    GIVEN a User model
    WHEN a new User is created
    THEN check that username, email, password and Flask-Login fields are correct
    """
    assert new_user.email == "testing@user.com"
    assert new_user.check_password("password")
    assert new_user.is_authenticated
    assert new_user.is_active
    assert new_user.is_valid("password", "password")
    assert not new_user.is_anonymous


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
