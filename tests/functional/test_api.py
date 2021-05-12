def test_get_user(test_client, init_database):
     """
     GIVEN a Flask application configured for testing
     WHEN the '/api/users/{id}' url is requested (GET)
     THEN check if the returned JSON is correct
     """
     response = test_client.get("/api/users/2")
     assert response.status_code == 200
     assert b"id" in response.data
     assert b"_username" in response.data
     assert not b"null" in response.data

     response = test_client.get("/api/users/5")
     assert response.status_code == 404
     

def test_get_users(test_client, init_database):
    """
     GIVEN a Flask application configured for testing
     WHEN the '/api/users' url is requested (GET)
     THEN check if the returned JSON is correct
     """
    response = test_client.get("/api/users")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"_username" in response.data
    assert not b"null" in response.data

def test_get_user_pastebins(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/users/{id}/pastebins' url is requested (GET)
    THEN check if the returned JSON is correct
    """
    response = test_client.get("/api/users/1/pastebins")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"link" in response.data
    assert b"content" in response.data
    assert b"syntax" in response.data

def test_get_user_private_pastebins(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/users/{id}/pastebins' url is requested (GET)
    THEN check if the returned JSON is correct
    """
    response = test_client.get("/api/users/2/pastebins")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"link" in response.data
    assert b"password" in response.data

    response = test_client.get("/api/users/5/pastebins")
    assert response.status_code == 404

def test_get_pastebin(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/pastebins/{id}' url is requested (GET)
    THEN check if the returned JSON is correct
    """
    response = test_client.get("/api/pastebins/2")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"link" in response.data
    assert b"password" in response.data

    response = test_client.get("/api/pastebins/5")
    assert response.status_code == 404
    
def test_get_pastebins(test_client, init_database):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/pastebins' url is requested (GET)
    THEN check if the returned JSON is correct
    """
    response = test_client.get("/api/pastebins")
    assert response.status_code == 200
    assert b"id" in response.data
    assert b"link" in response.data
    assert b"password" in response.data
