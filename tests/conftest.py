"""Pytest configuration and fixtures for API tests"""
import pytest
import copy
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path so we can import app
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Provide a TestClient instance for testing the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def fresh_activities():
    """
    Provide a fresh copy of the activities database for each test.
    This fixture resets the in-memory activities to initial state before each test.
    """
    # Store original state
    original_activities = copy.deepcopy(activities)
    
    # Reset activities to known state for testing
    activities.clear()
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
    })
    
    yield activities
    
    # Restore original state after test completes
    activities.clear()
    activities.update(original_activities)


@pytest.fixture
def client_with_fresh_data(client, fresh_activities):
    """
    Provide a TestClient with fresh activities data.
    Use this fixture in tests that need both a client and reset activities.
    """
    return client
