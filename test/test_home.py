def test_home(client):
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "Welcome to Organização Acadêmica API"
