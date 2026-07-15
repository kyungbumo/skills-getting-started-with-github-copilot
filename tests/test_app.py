from fastapi.testclient import TestClient
from src import app as app_module

client = TestClient(app_module.app)

def test_get_activities_returns_all_activities():
    # Arrange
    expected_names = {
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Swimming Club",
        "Art Club",
        "Drama Club",
        "Math Olympiad",
        "Science Club",
    }

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert expected_names.issubset(set(data.keys()))
    assert data["Chess Club"]["max_participants"] == 12

def test_signup_adds_participant_and_updates_activity():
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in app_module.activities[activity_name]["participants"]

def test_signup_existing_participant_returns_400():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={email}"
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_remove_participant_success():
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in app_module.activities[activity_name]["participants"]

def test_remove_nonexistent_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={email}"
    )

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found for this activity"
