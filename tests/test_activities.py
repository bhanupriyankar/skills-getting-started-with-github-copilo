"""Tests for the activities endpoint (GET /activities)

Using AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Execute the API call
- Assert: Verify the response
"""
import pytest


class TestActivitiesEndpoint:
    """Tests for retrieving the list of available activities"""

    def test_get_all_activities_returns_dict(self, client_with_fresh_data):
        """
        Test that GET /activities returns a dictionary of activities.
        
        Arrange: Create a test client with fresh activities data
        Act: Make a GET request to /activities
        Assert: Verify the response is a valid dictionary with expected keys
        """
        # Arrange
        # (client_with_fresh_data fixture is provided by conftest.py)
        
        # Act
        response = client_with_fresh_data.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert isinstance(activities_data, dict)

    def test_get_activities_includes_required_fields(self, client_with_fresh_data):
        """
        Test that each activity in the response has all required fields.
        
        Arrange: Create a test client with fresh activities data
        Act: Make a GET request to /activities
        Assert: Verify each activity has description, schedule, max_participants, and participants
        """
        # Arrange
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        # Act
        response = client_with_fresh_data.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_info in activities_data.items():
            assert isinstance(activity_name, str), f"Activity name should be string, got {type(activity_name)}"
            assert isinstance(activity_info, dict), f"Activity data should be dict, got {type(activity_info)}"
            assert required_fields.issubset(
                activity_info.keys()
            ), f"Activity '{activity_name}' missing required fields. Has: {activity_info.keys()}"

    def test_get_activities_participants_is_list(self, client_with_fresh_data):
        """
        Test that the participants field in each activity is a list.
        
        Arrange: Create a test client with fresh activities data
        Act: Make a GET request to /activities
        Assert: Verify each activity's participants field is a list
        """
        # Arrange
        # (client_with_fresh_data fixture is provided by conftest.py)
        
        # Act
        response = client_with_fresh_data.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, activity_info in activities_data.items():
            assert isinstance(
                activity_info["participants"], list
            ), f"Activity '{activity_name}' participants should be a list"

    def test_get_activities_contains_chess_club(self, client_with_fresh_data):
        """
        Test that the activities list includes Chess Club.
        
        Arrange: Create a test client with fresh activities data
        Act: Make a GET request to /activities
        Assert: Verify Chess Club is in the response with correct data
        """
        # Arrange
        # (client_with_fresh_data fixture is provided by conftest.py)
        
        # Act
        response = client_with_fresh_data.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        assert "Chess Club" in activities_data
        chess_club = activities_data["Chess Club"]
        assert chess_club["max_participants"] == 12
        assert "michael@mergington.edu" in chess_club["participants"]
        assert "daniel@mergington.edu" in chess_club["participants"]

    def test_get_activities_initial_participant_counts(self, client_with_fresh_data):
        """
        Test that initial participant counts are as expected.
        
        Arrange: Create a test client with fresh activities data
        Act: Make a GET request to /activities
        Assert: Verify each activity has the correct number of initial participants
        """
        # Arrange
        expected_participants_count = {
            "Chess Club": 2,
            "Programming Class": 2,
            "Gym Class": 2,
        }
        
        # Act
        response = client_with_fresh_data.get("/activities")
        activities_data = response.json()
        
        # Assert
        assert response.status_code == 200
        for activity_name, expected_count in expected_participants_count.items():
            actual_count = len(activities_data[activity_name]["participants"])
            assert actual_count == expected_count, \
                f"Activity '{activity_name}' should have {expected_count} participants, got {actual_count}"
