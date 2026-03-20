"""
API tests for High School Management System

Tests follow the AAA (Arrange-Act-Assert) pattern:
- Arrange: Set up test data and dependencies
- Act: Execute the API call
- Assert: Verify the response and state
"""

import pytest


class TestGetActivities:
    """Test suite for GET /activities endpoint"""
    
    def test_get_activities_returns_all_activities(self, client):
        # Arrange: No setup needed, activities are pre-populated
        
        # Act: Fetch all activities
        response = client.get("/activities")
        
        # Assert: Verify response status and content
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0
        assert "Chess Club" in data
        assert data["Chess Club"]["description"]
        assert "participants" in data["Chess Club"]


class TestSignupForActivity:
    """Test suite for POST /activities/{activity_name}/signup endpoint"""
    
    def test_signup_new_student_success(self, client, reset_activities):
        # Arrange: Define test data
        activity_name = "Chess Club"
        new_email = "newstudent@mergington.edu"
        
        # Act: Sign up student for activity
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        
        # Assert: Verify successful signup
        assert response.status_code == 200
        assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"
    
    def test_signup_duplicate_student_fails(self, client, reset_activities):
        # Arrange: Use existing participant from Chess Club
        activity_name = "Chess Club"
        existing_email = "michael@mergington.edu"
        
        # Act: Attempt to sign up student already registered
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": existing_email}
        )
        
        # Assert: Verify duplicate signup is rejected
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_nonexistent_activity_fails(self, client, reset_activities):
        # Arrange: Define invalid activity name and valid email
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act: Attempt to sign up for activity that doesn't exist
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert: Verify 404 error is returned
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestUnregisterFromActivity:
    """Test suite for DELETE /activities/{activity_name}/unregister endpoint"""
    
    def test_unregister_existing_participant_success(self, client, reset_activities):
        # Arrange: Use existing participant
        activity_name = "Chess Club"
        email = "michael@mergington.edu"
        
        # Act: Unregister participant from activity
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert: Verify successful unregistration
        assert response.status_code == 200
        assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    
    def test_unregister_nonexistent_participant_fails(self, client, reset_activities):
        # Arrange: Use email not registered for activity
        activity_name = "Chess Club"
        email = "notregistered@mergington.edu"
        
        # Act: Attempt to unregister participant not in activity
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert: Verify 400 error is returned
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"]
    
    def test_unregister_from_nonexistent_activity_fails(self, client, reset_activities):
        # Arrange: Define invalid activity and valid email
        activity_name = "Nonexistent Club"
        email = "student@mergington.edu"
        
        # Act: Attempt to unregister from activity that doesn't exist
        response = client.delete(
            f"/activities/{activity_name}/unregister",
            params={"email": email}
        )
        
        # Assert: Verify 404 error is returned
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]
