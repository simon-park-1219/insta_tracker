def test_list_notifications(client, auth_headers):
    # Create account and snapshots to generate notifications
    r = client.post("/api/accounts", json={"instagram_username": "notiftest"}, headers=auth_headers)
    acct_id = r.json()["id"]
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)

    r = client.get("/api/notifications", headers=auth_headers)
    assert r.status_code == 200
    assert isinstance(r.json(), list)


def test_mark_all_read(client, auth_headers):
    r = client.post("/api/accounts", json={"instagram_username": "readtest"}, headers=auth_headers)
    acct_id = r.json()["id"]
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)
    client.post(f"/api/accounts/{acct_id}/snapshots", headers=auth_headers)

    r = client.post("/api/notifications/read-all", headers=auth_headers)
    assert r.status_code == 200

    r = client.get("/api/notifications?unread_only=true", headers=auth_headers)
    assert len(r.json()) == 0


def test_changes_summary(client, auth_headers):
    r = client.get("/api/changes/summary", headers=auth_headers)
    assert r.status_code == 200
    assert "total_changes" in r.json()
