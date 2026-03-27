"""
Tests for the POST /activities/{activity_name}/signup endpoint.

This module tests student signup functionality including success cases and error handling.
"""

import pytest


def test_signup_success(client, sample_email):
    """
    Test: Successfully sign up a new student for an activity
    
    Arrange: Prepare test email and identify an activity with available space
    Act: Make POST request to signup endpoint with valid activity and new email
    Assert: Verify response is 200 and confirms signup
    """
    # Arrange
    activity_name = "Chess Club"
    new_email = "newstudent@mergington.edu"
    
    # Get initial participant count
    initial_response = client.get("/activities")
    initial_participants = initial_response.json()[activity_name]["participants"].copy()
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": new_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert new_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was added
    verify_response = client.get("/activities")
    updated_participants = verify_response.json()[activity_name]["participants"]
    assert new_email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_invalid_activity_returns_404(client):
    """
    Test: Signup to non-existent activity returns 404
    
    Arrange: Prepare invalid activity name
    Act: Make POST request to signup with non-existent activity
    Assert: Verify response is 404 with appropriate error message
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    test_email = "student@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{invalid_activity}/signup",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email_returns_400(client):
    """
    Test: Attempting to signup an already-registered student returns 400
    
    Arrange: Get an email already registered for an activity
    Act: Attempt to signup the same email again
    Assert: Verify response is 400 with appropriate error message
    """
    # Arrange
    activity_name = "Chess Club"
    # Get an existing participant from the activity
    activities_response = client.get("/activities")
    existing_email = activities_response.json()[activity_name]["participants"][0]
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": existing_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_signup_new_student_to_activity_with_capacity(client):
    """
    Test: Student can signup to activity that has available capacity
    
    Arrange: Select activity and prepare unique email
    Act: Sign up new student
    Assert: Verify signup was successful and student is in participants list
    """
    # Arrange
    activity_name = "Tennis Club"
    unique_email = "tennis_student_12345@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": unique_email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify in activities list
    activities = client.get("/activities").json()
    assert unique_email in activities[activity_name]["participants"]
