def test_get_wars_empty(client):
    """
    Test getting wars from an empty database.
    """
    response = client.get("/api/v1/war/")
    assert response.status_code == 200
    assert response.json() == []

def test_get_war_not_found(client):
    """
    Test getting a single war that does not exist.
    """
    response = client.get("/api/v1/war/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "War not found"
