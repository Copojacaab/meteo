"""
- creazione riuscita: 201
- lettura riuscita: 200
- aggiornamento riuscito: 200
- cancellazione riuscita: 204
- spot inesistente o appartenente a un altro utente: 404
- token assente, invalido o scaduto: 401
- dati JSON non validi: 422
"""

# ==== HELPER ====


async def _register_user(client, email):
    return await client.post(
        "/api/auth/register",
        json={"email": email, "password": "secret123"},
    )


async def _login_user(client, email):
    response = await client.post(
        "/api/auth/login",
        data={"username": email, "password": "secret123"},
    )

    return response.json()["access_token"]


async def _create_spot(client, token, name, lon, lat, radius):
    created = await client.post(
        "/api/spots",
        headers={"Authorization": f"Bearer {token}"},
        json={"name": name, "longitude": lon, "latitude": lat, "radius": radius},
    )

    return created


# ==== ====


# ==== Creazione  (Crud) ====
async def test_create_spot_returns_created_spot(api_client):
    email = "spot-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    response = await api_client.post(
        "/api/spots",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "name": "Bosco nord",
            "longitude": 11.5,
            "latitude": 44.5,
            "radius": 500,
        },
    )
    assert response.status_code == 201


# ---- No Auth ----
async def test_create_spot_requires_authentication(api_client):
    response = await api_client.post(
        "/api/spots",
        json={
            "name": "Bosco nord",
            "longitude": 11.5,
            "latitude": 44.5,
            "radius": 500,
        },
    )

    assert response.status_code == 401


# ==== Lettura (cRud) ====


async def test_read_spot_returns_owner_spot(api_client):
    email = "spot-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Mio Spot", 11.5, 44.5, 500)

    spot_id = created.json()["id"]

    response = await api_client.get(
        f"/api/spots/{spot_id}", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


async def test_read_spot_requires_authentication(api_client):
    email = "spot-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Mio Spot", 11.5, 44.5, 500)
    spot_id = created.json()["id"]

    response = api_client.get(f"/api/spots/{spot_id}")

    assert response.status_code == 401


async def test_list_spot_returns_owner_spot_list(api_client):
    email = "spot-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Mio SpotA", 11.5, 44.5, 500)
    created = await _create_spot(api_client, token, "Mio SpotB", 11.6, 44.6, 500)
    created = await _create_spot(api_client, token, "Mio SpotC", 11.7, 44.7, 500)

    response = await api_client.get(
        "/api/spots", headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200


async def test_list_spots_requires_authentiation(api_client):
    response = await api_client.get("/api/spots")

    assert response.status_code == 401


#

# ==== Aggiornamento (crUd) ====


async def test_update_spot_returns_updated_spot(api_client):
    email = "update-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Vecchio Nome", 11.5, 44.5, 500)
    spot_id = created.json()["id"]

    response = await api_client.put(
        f"/api/spots/{spot_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "new_name": "Nuovo Nome",
            "new_lon": 11.6,
            "new_lat": 44.6,
            "new_radius": 1000,
        },
    )

    assert response.status_code == 200

    body = response.json()
    assert body["id"] == spot_id
    assert body["name"] == "Nuovo Nome"
    assert body["longitude"] == 11.6
    assert body["latitude"] == 44.6
    assert body["radius"] == 1000


async def test_update_spot_requires_authentication(api_client):
    email = "update-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Vecchio Nome", 11.5, 44.5, 500)
    spot_id = created.json()["id"]

    response = api_client.put(
        f"/api/spots/{spot_id}",
        json={
            "new_name": "Nuovo Nome",
            "new_lon": 12.0,
            "new_lat": 45.0,
            "new_radius": 2000,
        },
    )

    assert response.status_code == 401


# ==== Cancellazione (cruD) ====
async def test_delete_spot_returns_no_content(api_client):
    email = "delete-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Da Eliminare", 11.5, 44.5, 500)
    spot_id = created.json()["id"]

    response = await api_client.delete(
        f"/api/spots/{spot_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 204
    assert response.content == b""

async def test_delete_spot_requires_authentication(api_client)
    email = "delete-owner@example.com"

    await _register_user(api_client, email)
    token = await _login_user(api_client, email)

    created = await _create_spot(api_client, token, "Da Eliminare", 11.5, 44.5, 500)
    spot_id = created.json()["id"]

    response = await api_client.delete(
        f"/api/spots/{spot_id}",
        headers={"Authorization": f"Bearer {token}"},
    )    

    assert response.status_code == 401

# ==== Ownership ====


async def test_other_user_cannot_read_spot(api_client):
    owner_email = "spot-owner@example.com"
    other_email = "other-owner@example.com"

    await _register_user(api_client, owner_email)
    await _register_user(api_client, other_email)

    owner_token = await _login_user(api_client, owner_email)
    other_token = await _login_user(api_client, other_email)

    created = await api_client.post(
        "/api/spots",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "name": "Spot Privato",
            "longitude": 11.5,
            "latitude": 44.5,
            "radius": 500,
        },
    )

    spot_id = created.json()["id"]

    response = await api_client.get(
        f"/api/spots/{spot_id}", headers={"Authorization": f"Bearer {other_token}"}
    )

    assert response.status_code == 404


async def test_other_user_cannot_list_spots(api_client): ...
