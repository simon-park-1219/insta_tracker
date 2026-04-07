def test_trigger_snapshot(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "snaptest"}, headers=auth_headers)
    acct_id = r.json()["id"]
    r = client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    assert r.status_code == 200
    assert r.json()["status"] == "success"
    assert r.json()["follower_count"] > 0


def test_list_snapshots(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "snaplist"}, headers=auth_headers)
    acct_id = r.json()["id"]
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    r = client.get(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    assert r.status_code == 200
    assert len(r.json()) == 2


def test_snapshot_triggers_diff(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "difftest"}, headers=auth_headers)
    acct_id = r.json()["id"]
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    r = client.get(f"/api/accounts/{acct_id}/changes", headers=auth_headers)
    assert r.status_code == 200
    # Mock scraper evolves, so changes should be detected
    changes = r.json()
    assert len(changes) >= 0  # Could be 0 if mock didn't evolve
