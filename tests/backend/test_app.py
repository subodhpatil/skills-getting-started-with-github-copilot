from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    activity_name = "Chess Club"
    original_participants = list(activities[activity_name]["participants"])
    participant_email = original_participants[0]

    try:
        # Act
        response = client.delete(
            f"/activities/{activity_name}/participants/{participant_email}"
        )

        # Assert
        assert response.status_code == 200
        assert participant_email not in activities[activity_name]["participants"]
        assert response.json()["message"] == f"Unregistered {participant_email} from {activity_name}"
    finally:
        activities[activity_name]["participants"] = original_participants


def test_unregister_participant_returns_404_when_not_registered():
    # Arrange
    activity_name = "Chess Club"
    email = "not-a-student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/participants/{email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
