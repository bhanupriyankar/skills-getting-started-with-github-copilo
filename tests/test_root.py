"""Tests for the root endpoint (GET /)

Using AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Execute the API call
- Assert: Verify the response
"""
import pytest


class TestRootEndpoint:
    """Tests for the root endpoint that redirects to static HTML"""

    def test_root_redirects_to_static_html(self, client):
        """
        Test that GET / redirects to the static index.html page.
        
        Arrange: Create a test client
        Act: Make a GET request to /
        Assert: Verify the response is a redirect (307) to /static/index.html
        """
        # Arrange
        # (client fixture is provided by conftest.py)
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"

    def test_root_with_follow_redirects(self, client):
        """
        Test that following the redirect from / loads the index.html page.
        
        Arrange: Create a test client
        Act: Make a GET request to / with follow_redirects=True
        Assert: Verify we get a 200 response (successful load of index.html)
        """
        # Arrange
        # (client fixture is provided by conftest.py)
        
        # Act
        response = client.get("/", follow_redirects=True)
        
        # Assert
        assert response.status_code == 200
        assert "Mergington High School" in response.text
