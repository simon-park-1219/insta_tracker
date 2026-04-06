def test_create_account(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "testaccount"}, headers=auth_headers)
    assert r.status_code == 201
    assert r.json()["instagram_username"] == "testaccount"


def test_list_accounts(client, auth_headers):
    client.post("/api/accounts", json={"instagram_username": "acc1"}, headers=auth_headers)
    client.post("/api/accounts", json={"instagram_username": "acc2"}, headers=auth_headers)
    r = client.get("/api/accounts", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_get_account(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "gettest"}, headers=auth_headers)
    acct_id = r.json()["id"]
    r = client.get(f"/api/accounts/{acct_id}", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["instagram_username"] == "gettest"


def test_update_account(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "upd"}, headers=auth_headers)
    acct_id = r.json()["id"]
    r = client.patch(f"/api/accounts/{acct_id}", json={"is_active": False}, headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["is_active"] is False


def test_delete_account(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "del"}, headers=auth_headers)
    acct_id = r.json()["id"]
    r = client.delete(f"/api/accounts/{acct_id}", headers=auth_headers)
    assert r.status_code == 204


def test_account_not_found(client, auth_headers):
    r = client.get("/api/accounts/nonexistent", headers=auth_headers)
    assert r.status_code == 404
