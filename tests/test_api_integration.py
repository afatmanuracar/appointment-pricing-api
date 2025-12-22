import pytest

HEADERS = {"X-API-Key": "dev-secret-key"}

@pytest.mark.anyio
async def test_health(client):
    r = await client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"ok": True}

@pytest.mark.anyio
async def test_create_member_class_and_reservation(client):
    m = await client.post(
        "/members",
        json={"name": "Alice", "membership_type": "standard"},
        headers=HEADERS,
    )
    assert m.status_code == 201
    member_id = m.json()["id"]

    c = await client.post(
        "/classes",
        json={
            "name": "Yoga",
            "instructor": "Coach",
            "capacity": 2,
            "start_time": "2025-12-01T10:00:00",
        },
        headers=HEADERS,
    )
    assert c.status_code == 201
    class_id = c.json()["id"]

    r = await client.post(
        "/reservations",
        json={
            "member_id": member_id,
            "class_id": class_id,
            "base_price": 100,
        },
        headers=HEADERS,
    )
    assert r.status_code == 201

@pytest.mark.anyio
async def test_capacity_full_returns_409(client):
    m1 = await client.post(
        "/members",
        json={"name": "A", "membership_type": "standard"},
        headers=HEADERS,
    )
    m2 = await client.post(
        "/members",
        json={"name": "B", "membership_type": "standard"},
        headers=HEADERS,
    )

    class_resp = await client.post(
        "/classes",
        json={
            "name": "Pilates",
            "instructor": "Coach",
            "capacity": 1,
            "start_time": "2025-12-01T10:00:00",
        },
        headers=HEADERS,
    )

    class_id = class_resp.json()["id"]

    ok = await client.post(
        "/reservations",
        json={"member_id": m1.json()["id"], "class_id": class_id, "base_price": 100},
        headers=HEADERS,
    )
    assert ok.status_code == 201

    full = await client.post(
        "/reservations",
        json={"member_id": m2.json()["id"], "class_id": class_id, "base_price": 100},
        headers=HEADERS,
    )
    assert full.status_code == 409

# 🔐 AUTH TESTLERİ

@pytest.mark.anyio
async def test_post_requires_api_key(client):
    r = await client.post(
        "/members",
        json={"name": "NoKey", "membership_type": "standard"},
    )
    assert r.status_code == 401
    assert r.json()["detail"] == "Unauthorized"

@pytest.mark.anyio
async def test_post_rejects_wrong_api_key(client):
    r = await client.post(
        "/members",
        json={"name": "WrongKey", "membership_type": "standard"},
        headers={"X-API-Key": "wrong-key"},
    )
    assert r.status_code == 401
