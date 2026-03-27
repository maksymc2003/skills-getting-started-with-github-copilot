"""
Tests for the root endpoint (GET /).

This module tests the root endpoint which should redirect to the static index.html file.
"""

from fastapi.testclient import TestClient


def test_root_redirects_to_index(client):
    """
    Test: GET / should redirect to /static/index.html
    
    Arrange: Prepare the TestClient (provided by fixture)
    Act: Make a GET request to the root endpoint
    Assert: Verify status code is 307 (temporary redirect) and location header is correct
    """
    # Arrange, Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_root_follows_redirect(client):
    """
    Test: GET / should eventually reach the static index file
    
    Arrange: Prepare the TestClient (provided by fixture)
    Act: Make a GET request to the root endpoint with redirect following
    Assert: Verify we can successfully follow the redirect
    """
    # Arrange, Act
    response = client.get("/", follow_redirects=True)
    
    # Assert - Should reach the static file (200 status)
    assert response.status_code == 200
