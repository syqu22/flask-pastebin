# """
# This file contains the functional tests for the auth blueprint.
# """

# def test_login_page(test_client):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get("/login")
#     assert response.status_code == 200
#     assert b"Username" in response.data
#     assert b"Password" in response.data

# def test_valid_login_and_logout(test_client, init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/login' page is posted (POST)
#     THEN check the response is valid
#     """
#     response = test_client.post("/login", data=dict(username="user1", password="password"), follow_redirects=True)

#     assert response.status_code == 200
#     assert b"Logged in successfully!" in response.data

#     """
#     GIVEN a Flask application configured for testing
#     WHEN the '/logout' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get("/logout", follow_redirects=True)
#     assert response.status_code == 200
#     assert b"Login" in response.data
#     assert b"Sign Up" in response.data

# def test_invalid_login(test_client, init_database):
#     """
#     GIVEN a Flask application configured for testing
#     WHEN the "/login" page is posted to with invalid credentials (POST)
#     THEN check an error message is returned to the user
#     """
#     response = test_client.post("/login", data=dict(username="wrong_user", password="password"), follow_redirects=True)
    
#     assert response.status_code == 200
#     assert b"User with this name does not exist." in response.data
#     assert b"Login" in response.data
#     assert b"Sign Up" in response.data
