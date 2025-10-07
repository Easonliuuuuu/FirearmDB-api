def test_get_manufacturers_empty(client):
    """
    Test getting manufacturers from an empty database.
    """
    response = client.get("/api/v1/manufacturer/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_manufacturer_not_found(client):
    """
    Test getting a single manufacturer that does not exist.
    """
    response = client.get("/api/v1/manufacturer/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Manufacturer not found"
