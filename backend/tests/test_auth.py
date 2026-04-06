def test_register(client):
    r = client.post("/api/auth/register", json={"email": "new@test.com", "password": "pass1234"})
    assert r.status_code == 201
    assert "access_token" in r.json()


def test_register_duplicate(client):
    client.post("/api/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    r = client.post("/api/auth/register", json={"email": "dup@test.com", "password": "pass1234"})
    assert r.status_code == 400


def test_login(client):
    client.post("/api/auth/register", json={"email": "login@test.com", "password": "pass1234"})
    r = client.post("/api/auth/login", json={"email": "login@test.com", "password": "pass1234"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_login_wrong_password(client):
    client.post("/api/auth/register", json={"email": "wrong@test.com", "password": "pass1234"})
    r = client.post("/api/auth/login", json={"email": "wrong@test.com", "password": "wrongpass"})
    assert r.status_code == 401


def test_get_me(client, auth_headers):
    r = client.get("/api/auth/me", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["email"] == "test@test.com"


def test_get_me_no_token(client):
    r = client.get("/api/auth/me")
    assert r.status_code in (401, 403)
