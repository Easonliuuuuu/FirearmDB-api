def test_get_cartridges_empty(client):
    """
    Test getting cartridges from an empty database.
    """
    response = client.get("/api/v1/cartridge/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_cartridge_not_found(client):
    """
    Test getting a single cartridge that does not exist.
    """
    response = client.get("/api/v1/cartridge/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Cartridge not found"
