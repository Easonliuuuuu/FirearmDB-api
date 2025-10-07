def test_get_types_empty(client):
    """
    Test getting firearm types from an empty database.
    """
    response = client.get("/api/v1/type/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_type_not_found(client):
    """
    Test getting a single type that does not exist.
    """
    response = client.get("/api/v1/type/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Type not found"
