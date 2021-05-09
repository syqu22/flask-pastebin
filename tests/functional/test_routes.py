"""
This file contains the functional tests for the pastebin_view blueprint.
"""
from web import create_app


def test_home_page():
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is requested (GET)
    THEN check that the response is valid
    """
    flask_app = create_app()
    flask_app.config["TESTING"] = True

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        response = test_client.get("/")
        assert response.status_code == 200

def test_home_page_with_fixture(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the "/" page is requested (GET)
    THEN check that the response is valid
    """
    response = test_client.get("/")
    assert response.status_code == 200
