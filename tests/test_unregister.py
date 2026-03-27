"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.

This module tests student unregistration functionality including success cases and error handling.
"""

import pytest


def test_unregister_success(client):
    """
    Test: Successfully unregister a student from an activity
    
    Arrange: Sign up a student, then prepare to unregister them
    Act: Make DELETE request to unregister endpoint with valid activity and email
    Assert: Verify response is 200 and student is removed from participants
    """
    # Arrange
    activity_name = "Science Club"
    test_email = "unregister_test@mergington.edu"
    
    # First, sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Verify signup was successful
    activities = client.get("/activities").json()
    assert test_email in activities[activity_name]["participants"]
    initial_count = len(activities[activity_name]["participants"])
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert test_email in data["message"]
    assert activity_name in data["message"]
    
    # Verify participant was removed
    verify_response = client.get("/activities")
    final_participants = verify_response.json()[activity_name]["participants"]
    assert test_email not in final_participants
    assert len(final_participants) == initial_count - 1


def test_unregister_invalid_activity_returns_404(client):
    """
    Test: Unregister from non-existent activity returns 404
    
    Arrange: Prepare invalid activity name
    Act: Make DELETE request to unregister with non-existent activity
    Assert: Verify response is 404 with appropriate error message
    """
    # Arrange
    invalid_activity = "Nonexistent Club"
    test_email = "student@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{invalid_activity}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered_student_returns_400(client):
    """
    Test: Attempting to unregister a non-registered student returns 400
    
    Arrange: Prepare an email that is not registered for the activity
    Act: Attempt to unregister the non-registered email
    Assert: Verify response is 400 with appropriate error message
    """
    # Arrange
    activity_name = "Music Ensemble"
    non_registered_email = "not_signed_up@mergington.edu"
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": non_registered_email}
    )
    
    # Assert
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "not signed up" in data["detail"].lower()


def test_unregister_registered_student(client):
    """
    Test: Successfully unregister a student who is currently registered
    
    Arrange: Sign up a student, then unregister them
    Act: Unregister the student
    Assert: Verify the student is removed from the activity's participant list
    """
    # Arrange
    activity_name = "Debate Team"
    test_email = "debate_student_99999@mergington.edu"
    
    # Sign up the student
    client.post(
        f"/activities/{activity_name}/signup",
        params={"email": test_email}
    )
    
    # Verify they're signed up
    before = client.get("/activities").json()
    assert test_email in before[activity_name]["participants"]
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/unregister",
        params={"email": test_email}
    )
    
    # Assert
    assert response.status_code == 200
    
    # Verify they're removed
    after = client.get("/activities").json()
    assert test_email not in after[activity_name]["participants"]
