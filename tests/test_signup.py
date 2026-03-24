"""Tests for the signup endpoint (POST /activities/{activity_name}/signup)

Using AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test fixtures and data
- Act: Execute the API call
- Assert: Verify the response
"""
import pytest


class TestSignupEndpoint:
    """Tests for signing up a student for an activity"""

    def test_successful_signup(self, client_with_fresh_data):
        """
        Test that a student can successfully sign up for an activity.
        
        Arrange: Create a test client with fresh data and a new student email
        Act: Make a POST request to signup for Chess Club
        Assert: Verify the response is successful and includes confirmation message
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "newstudent@mergington.edu"
        
        # Act
        response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert "message" in response_data
        assert student_email in response_data["message"]
        assert activity_name in response_data["message"]

    def test_signup_adds_participant_to_activity(self, client_with_fresh_data):
        """
        Test that signup actually adds the participant to the activity's participant list.
        
        Arrange: Create a test client with fresh data and a new student email
        Act: Make a POST request to signup, then GET activities to verify
        Assert: Verify the student is now in the participants list
        """
        # Arrange
        activity_name = "Chess Club"
        student_email = "newstudent@mergington.edu"
        
        # Act
        response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        activities_response = client_with_fresh_data.get("/activities")
        activities_data = activities_response.json()
        
        # Assert
        assert response.status_code == 200
        assert student_email in activities_data[activity_name]["participants"]

    def test_signup_fails_for_nonexistent_activity(self, client_with_fresh_data):
        """
        Test that signing up for a non-existent activity returns 404.
        
        Arrange: Create a test client and use a fake activity name
        Act: Make a POST request to signup for a non-existent activity
        Assert: Verify the response is a 404 error with appropriate message
        """
        # Arrange
        nonexistent_activity = "Underwater Basket Weaving"
        student_email = "student@mergington.edu"
        
        # Act
        response = client_with_fresh_data.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 404
        response_data = response.json()
        assert "detail" in response_data or "message" in response_data

    def test_signup_fails_for_duplicate_email(self, client_with_fresh_data):
        """
        Test that a student cannot sign up twice for the same activity.
        
        Arrange: Create a test client and use an already-registered student
        Act: Try to signup for an activity they're already in
        Assert: Verify the response is a 400 error indicating duplicate signup
        """
        # Arrange
        activity_name = "Chess Club"
        # michael@mergington.edu is already in Chess Club (from fresh_activities fixture)
        duplicate_email = "michael@mergington.edu"
        
        # Act
        response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": duplicate_email}
        )
        
        # Assert
        assert response.status_code == 400
        response_data = response.json()
        assert "detail" in response_data or "message" in response_data
        assert "already signed up" in response_data.get("detail", "").lower()

    def test_signup_with_special_characters_in_email(self, client_with_fresh_data):
        """
        Test that signup works with valid email addresses containing special characters.
        
        Arrange: Create a test client and use an email with special characters
        Act: Make a POST request with an email containing dots and plus signs
        Assert: Verify the signup is successful
        """
        # Arrange
        activity_name = "Programming Class"
        # Email with special characters that are valid
        special_email = "john.doe+period@mergington.edu"
        
        # Act
        response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": special_email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert special_email in response_data["message"]

    def test_signup_multiple_students_same_activity(self, client_with_fresh_data):
        """
        Test that multiple different students can sign up for the same activity.
        
        Arrange: Create a test client and multiple new student emails
        Act: Sign up three different students for the same activity
        Assert: Verify all three students are added successfully
        """
        # Arrange
        activity_name = "Gym Class"
        students = ["alice@mergington.edu", "bob@mergington.edu", "charlie@mergington.edu"]
        
        # Act
        for student_email in students:
            response = client_with_fresh_data.post(
                f"/activities/{activity_name}/signup",
                params={"email": student_email}
            )
            # Assert after each signup
            assert response.status_code == 200
        
        # Verify all students are now registered
        activities_response = client_with_fresh_data.get("/activities")
        activities_data = activities_response.json()
        participants = activities_data[activity_name]["participants"]
        
        for student_email in students:
            assert student_email in participants

    def test_signup_increments_participant_count(self, client_with_fresh_data):
        """
        Test that signup correctly increments the participant count.
        
        Arrange: Get initial participant count, create client and new student email
        Act: Sign up new student, then get updated participant count
        Assert: Verify participant count increased by exactly 1
        """
        # Arrange
        activity_name = "Programming Class"
        new_student = "future@mergington.edu"
        
        # Get initial count
        initial_response = client_with_fresh_data.get("/activities")
        initial_data = initial_response.json()
        initial_count = len(initial_data[activity_name]["participants"])
        
        # Act
        signup_response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_student}
        )
        
        # Get updated count
        updated_response = client_with_fresh_data.get("/activities")
        updated_data = updated_response.json()
        updated_count = len(updated_data[activity_name]["participants"])
        
        # Assert
        assert signup_response.status_code == 200
        assert updated_count == initial_count + 1

    def test_signup_with_url_encoded_activity_name(self, client_with_fresh_data):
        """
        Test that signup works with activity names that need URL encoding (spaces, special chars).
        
        Arrange: Create a test client and use an activity with spaces in the name
        Act: Make a POST request with proper URL encoding for the activity name
        Assert: Verify the signup works correctly
        """
        # Arrange
        activity_name = "Programming Class"  # Contains a space
        student_email = "coder@mergington.edu"
        
        # Act
        # TestClient should handle URL encoding automatically
        response = client_with_fresh_data.post(
            f"/activities/{activity_name}/signup",
            params={"email": student_email}
        )
        
        # Assert
        assert response.status_code == 200
        response_data = response.json()
        assert student_email in response_data["message"]
