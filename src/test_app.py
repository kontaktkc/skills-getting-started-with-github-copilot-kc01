"""
Test suite for the Mergington High School Activities API

This test file demonstrates GitHub Copilot's ability to:
- Generate comprehensive test cases
- Create test data and fixtures
- Test various scenarios including edge cases
- Write clear test descriptions
"""

import pytest
from fastapi.testclient import TestClient
from app import app, activities, is_valid_email, check_activity_availability, is_already_signed_up

# Create a test client for the FastAPI application
client = TestClient(app)


class TestEmailValidation:
    """Test cases for email validation functionality"""
    
    def test_valid_mergington_email(self):
        """Test that valid mergington.edu emails are accepted"""
        assert is_valid_email("student@mergington.edu") is True
        assert is_valid_email("john.doe@mergington.edu") is True
        assert is_valid_email("test123@mergington.edu") is True
    
    def test_invalid_domain(self):
        """Test that emails from other domains are rejected"""
        assert is_valid_email("student@gmail.com") is False
        assert is_valid_email("student@otherschool.edu") is False
        assert is_valid_email("student@mergington.com") is False
    
    def test_invalid_email_format(self):
        """Test that malformed email addresses are rejected"""
        assert is_valid_email("notanemail") is False
        assert is_valid_email("@mergington.edu") is False
        assert is_valid_email("student@") is False
        assert is_valid_email("") is False


class TestActivityAvailability:
    """Test cases for activity availability checking"""
    
    def setup_method(self):
        """Reset activities data before each test"""
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    def test_activity_has_available_spots(self):
        """Test that activities with available spots return True"""
        assert check_activity_availability("Chess Club") is True
    
    def test_activity_is_full(self):
        """Test that full activities return False"""
        # Fill up Chess Club
        max_participants = activities["Chess Club"]["max_participants"]
        activities["Chess Club"]["participants"] = [f"student{i}@mergington.edu" for i in range(max_participants)]
        
        assert check_activity_availability("Chess Club") is False
    
    def test_nonexistent_activity(self):
        """Test that checking a nonexistent activity returns False"""
        assert check_activity_availability("Nonexistent Club") is False


class TestSignupStatus:
    """Test cases for checking if a student is already signed up"""
    
    def setup_method(self):
        """Reset activities data before each test"""
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    def test_student_is_signed_up(self):
        """Test that function correctly identifies signed up students"""
        assert is_already_signed_up("Chess Club", "michael@mergington.edu") is True
    
    def test_student_not_signed_up(self):
        """Test that function correctly identifies students not signed up"""
        assert is_already_signed_up("Chess Club", "newstudent@mergington.edu") is False
    
    def test_nonexistent_activity(self):
        """Test that checking signup for nonexistent activity returns False"""
        assert is_already_signed_up("Nonexistent Club", "student@mergington.edu") is False


class TestAPIEndpoints:
    """Test cases for API endpoints"""
    
    def setup_method(self):
        """Reset activities data before each test"""
        activities["Chess Club"]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]
        activities["Programming Class"]["participants"] = ["emma@mergington.edu", "sophia@mergington.edu"]
        activities["Gym Class"]["participants"] = ["john@mergington.edu", "olivia@mergington.edu"]
    
    def test_root_redirects_to_index(self):
        """Test that root endpoint redirects to static index page"""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307  # Redirect status
        assert "/static/index.html" in response.headers["location"]
    
    def test_get_all_activities(self):
        """Test retrieving all activities"""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert "Gym Class" in data
    
    def test_get_specific_activity(self):
        """Test retrieving details of a specific activity"""
        response = client.get("/activities/Chess Club")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Chess Club"
        assert "description" in data
        assert "spots_available" in data
        assert data["max_participants"] == 12
    
    def test_get_nonexistent_activity(self):
        """Test that requesting a nonexistent activity returns 404"""
        response = client.get("/activities/Nonexistent Club")
        assert response.status_code == 404
    
    def test_get_activity_participants(self):
        """Test retrieving participants for an activity"""
        response = client.get("/activities/Chess Club/participants")
        assert response.status_code == 200
        data = response.json()
        assert data["activity"] == "Chess Club"
        assert data["participant_count"] == 2
        assert "michael@mergington.edu" in data["participants"]
    
    def test_successful_signup(self):
        """Test successful student signup for an activity"""
        response = client.post("/activities/Chess Club/signup?email=newstudent@mergington.edu")
        assert response.status_code == 200
        data = response.json()
        assert "Successfully signed up" in data["message"]
        assert data["email"] == "newstudent@mergington.edu"
        assert "spots_remaining" in data
        
        # Verify student was added
        assert "newstudent@mergington.edu" in activities["Chess Club"]["participants"]
    
    def test_signup_with_invalid_email(self):
        """Test that signup with invalid email format is rejected"""
        response = client.post("/activities/Chess Club/signup?email=invalid@gmail.com")
        assert response.status_code == 400
        assert "Invalid email format" in response.json()["detail"]
    
    def test_signup_for_nonexistent_activity(self):
        """Test that signup for nonexistent activity returns 404"""
        response = client.post("/activities/Nonexistent Club/signup?email=student@mergington.edu")
        assert response.status_code == 404
    
    def test_duplicate_signup(self):
        """Test that duplicate signup is prevented"""
        email = "michael@mergington.edu"
        response = client.post(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]
    
    def test_signup_for_full_activity(self):
        """Test that signup for a full activity is rejected"""
        # Fill up Chess Club
        max_participants = activities["Chess Club"]["max_participants"]
        activities["Chess Club"]["participants"] = [f"student{i}@mergington.edu" for i in range(max_participants)]
        
        response = client.post("/activities/Chess Club/signup?email=latestudent@mergington.edu")
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()
    
    def test_successful_signup_removal(self):
        """Test successful removal of a student signup"""
        email = "michael@mergington.edu"
        response = client.delete(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 200
        data = response.json()
        assert "Successfully removed" in data["message"]
        
        # Verify student was removed
        assert email not in activities["Chess Club"]["participants"]
    
    def test_remove_signup_for_nonexistent_activity(self):
        """Test that removing signup from nonexistent activity returns 404"""
        response = client.delete("/activities/Nonexistent Club/signup?email=student@mergington.edu")
        assert response.status_code == 404
    
    def test_remove_signup_not_signed_up(self):
        """Test that removing a student who isn't signed up returns 400"""
        email = "notsignedup@mergington.edu"
        response = client.delete(f"/activities/Chess Club/signup?email={email}")
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]


class TestEdgeCases:
    """Test cases for edge cases and boundary conditions"""
    
    def setup_method(self):
        """Reset activities data before each test"""
        activities["Chess Club"]["participants"] = ["michael@mergington.edu"]
    
    def test_activity_name_with_spaces(self):
        """Test that activity names with spaces are handled correctly"""
        response = client.get("/activities/Chess Club")
        assert response.status_code == 200
    
    def test_email_case_sensitivity(self):
        """Test email validation with different cases"""
        # Note: Current implementation is case-sensitive
        response = client.post("/activities/Chess Club/signup?email=NewStudent@mergington.edu")
        assert response.status_code == 200
    
    def test_last_spot_in_activity(self):
        """Test signup when only one spot remains"""
        # Fill activity to one spot remaining
        max_participants = activities["Chess Club"]["max_participants"]
        activities["Chess Club"]["participants"] = [f"student{i}@mergington.edu" for i in range(max_participants - 1)]
        
        # This should succeed
        response = client.post("/activities/Chess Club/signup?email=lastone@mergington.edu")
        assert response.status_code == 200
        assert response.json()["spots_remaining"] == 0
        
        # Next signup should fail
        response = client.post("/activities/Chess Club/signup?email=toolate@mergington.edu")
        assert response.status_code == 400


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v"])
