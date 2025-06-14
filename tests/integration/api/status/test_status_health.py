def test_health_status(client):
    """
    Test for /status/healthcheck endpoint to ensure it returns a 204 status code
    """
    response = client.get("/status/healthcheck")

    assert response.status_code == 204
    assert response.content == b""
