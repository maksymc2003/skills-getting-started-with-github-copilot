"""
Tests for the GET /activities endpoint.

This module tests retrieving all available activities from the API.
"""


def test_get_activities_returns_all_activities(client):
    """
    Test: GET /activities should return all available activities
    
    Arrange: Prepare the TestClient (provided by fixture)
    Act: Make a GET request to /activities endpoint
    Assert: Verify response is 200 and contains all expected activities
    """
    # Arrange, Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    activities = response.json()
    
    # Verify we have activities
    assert len(activities) > 0
    
    # Verify expected activities are present
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Music Ensemble",
        "Debate Team",
        "Science Club"
    ]
    for activity in expected_activities:
        assert activity in activities


def test_activity_structure(client):
    """
    Test: Each activity should have the correct structure
    
    Arrange: Prepare the TestClient (provided by fixture)
    Act: Make a GET request to /activities endpoint
    Assert: Verify each activity has required fields with correct types
    """
    # Arrange, Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert - Check structure of first activity as representative sample
    first_activity_name = list(activities.keys())[0]
    activity = activities[first_activity_name]
    
    # Verify required fields exist
    assert "description" in activity
    assert "schedule" in activity
    assert "max_participants" in activity
    assert "participants" in activity
    
    # Verify field types
    assert isinstance(activity["description"], str)
    assert isinstance(activity["schedule"], str)
    assert isinstance(activity["max_participants"], int)
    assert isinstance(activity["participants"], list)


def test_activities_have_participants(client):
    """
    Test: Verify activities have participant data
    
    Arrange: Prepare the TestClient (provided by fixture)
    Act: Make a GET request to /activities endpoint
    Assert: Verify activities contain participant information
    """
    # Arrange, Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert - Verify participants structure
    for activity_name, activity_data in activities.items():
        participants = activity_data["participants"]
        assert isinstance(participants, list)
        # Each participant should be an email string
        for participant in participants:
            assert isinstance(participant, str)
            assert "@" in participant  # Simple email validation
