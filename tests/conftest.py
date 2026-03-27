"""
Pytest configuration and fixtures for FastAPI app tests.

This module provides shared fixtures for testing the Mergington High School API.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Fixture: TestClient instance for making HTTP requests to the FastAPI app.
    
    Returns a TestClient that can be used to make requests to the app
    in a test environment without running a server.
    """
    return TestClient(app)


@pytest.fixture
def sample_email():
    """
    Fixture: A sample email string for testing user signup.
    
    Returns a test email that can be used across multiple tests.
    """
    return "test@mersington.edu"
