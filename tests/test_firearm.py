
def test_get_firearms_empty(client):
    """
    Test getting firearms from an empty database.
    """
    response = client.get("/api/v1/firearm/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_firearm_not_found(client):
    """
    Test getting a single firearm that does not exist.
    """
    response = client.get("/api/v1/firearm/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Firearm not found"

def test_search_firearms_not_found(client):
    """
    Test searching for a firearm that doesn't exist.
    """
    response = client.get("/api/v1/firearm/search?name=nonexistent")
    assert response.status_code == 404
    assert response.json()["detail"] == "No firearms found matching the search criteria"
