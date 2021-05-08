def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200

def test_pastebin_route(client):
    response = client.get("/1")
    assert response.status_code == 200

def test_raw_pastebin_route(client):
    response = client.get("/raw/1")
    assert response.status_code == 200

def test_download_pastebin_route(client):
    response = client.get("/download/4")
    assert response.status_code == 200

def test_delete_pastebin_route(client):
    response = client.get("/delete/1")
    assert response.status_code == 200

def test_login_route(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_signup_route(client):
    response = client.get("/sign-up")
    assert response.status_code == 200
