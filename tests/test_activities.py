def test_get_activities_returns_seeded_activities(client):
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert "Programming Class" in activities
    assert set(activities["Chess Club"]) == {
        "description",
        "schedule",
        "max_participants",
        "participants",
    }
    assert "michael@mergington.edu" in activities["Chess Club"]["participants"]


def test_signup_adds_participant(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Signed up {email} for Chess Club"}
    activities = client.get("/activities").json()
    assert email in activities["Chess Club"]["participants"]


def test_signup_rejects_duplicate_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post("/activities/Chess Club/signup", params={"email": email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {"detail": "Student already signed up for this activity"}


def test_signup_rejects_unknown_activity(client):
    # Act
    response = client.post(
        "/activities/Unknown Activity/signup",
        params={"email": "new.student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_requires_email(client):
    # Act
    response = client.post("/activities/Chess Club/signup")

    # Assert
    assert response.status_code == 422


def test_unregister_removes_participant(client):
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {"message": f"Unregistered {email} from Chess Club"}
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]


def test_unregister_rejects_unknown_participant(client):
    # Act
    response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": "not.enrolled@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Student is not signed up for this activity"}


def test_unregister_rejects_unknown_activity(client):
    # Act
    response = client.delete(
        "/activities/Unknown Activity/participants",
        params={"email": "student@mergington.edu"},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_requires_email(client):
    # Act
    response = client.delete("/activities/Chess Club/participants")

    # Assert
    assert response.status_code == 422


def test_participant_can_signup_and_unregister(client):
    # Arrange
    email = "new.student@mergington.edu"

    # Act
    signup_response = client.post(
        "/activities/Chess Club/signup",
        params={"email": email},
    )
    unregister_response = client.delete(
        "/activities/Chess Club/participants",
        params={"email": email},
    )

    # Assert
    assert signup_response.status_code == 200
    assert unregister_response.status_code == 200
    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]