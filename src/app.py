"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.

This application demonstrates various GitHub Copilot capabilities including:
- Code completion and generation
- Documentation generation
- Error handling patterns
- Input validation
- API endpoint creation
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from typing import Dict, List, Optional
import os
import re
from pathlib import Path

app = FastAPI(title="Mergington High School API",
              description="API for viewing and signing up for extracurricular activities")

# Mount the static files directory
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(Path(__file__).parent,
          "static")), name="static")

# In-memory activity database
activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    }
}


def is_valid_email(email: str) -> bool:
    """
    Validate if the provided email is in correct format and from mergington.edu domain.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if email is valid and from mergington.edu domain, False otherwise
    """
    # Check basic email format
    email_pattern = r'^[a-zA-Z0-9._%+-]+@mergington\.edu$'
    return re.match(email_pattern, email) is not None


def check_activity_availability(activity_name: str) -> bool:
    """
    Check if an activity has available spots for new participants.
    
    Args:
        activity_name: Name of the activity to check
        
    Returns:
        True if spots are available, False otherwise
    """
    if activity_name not in activities:
        return False
    
    activity = activities[activity_name]
    current_participants = len(activity["participants"])
    max_participants = activity["max_participants"]
    
    return current_participants < max_participants


def is_already_signed_up(activity_name: str, email: str) -> bool:
    """
    Check if a student is already signed up for a specific activity.
    
    Args:
        activity_name: Name of the activity
        email: Student's email address
        
    Returns:
        True if student is already signed up, False otherwise
    """
    if activity_name not in activities:
        return False
    
    return email in activities[activity_name]["participants"]


@app.get("/")
def root():
    """
    Root endpoint that redirects to the main application page.
    
    Returns:
        RedirectResponse to the static index.html page
    """
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    """
    Get all available activities with their details.
    
    Returns:
        Dictionary of all activities with their information including:
        - description: Activity description
        - schedule: When the activity meets
        - max_participants: Maximum number of students allowed
        - participants: List of signed up student emails
    """
    return activities


@app.get("/activities/{activity_name}")
def get_activity_details(activity_name: str):
    """
    Get detailed information about a specific activity.
    
    Args:
        activity_name: Name of the activity to retrieve
        
    Returns:
        Dictionary with activity details and availability information
        
    Raises:
        HTTPException: 404 if activity is not found
    """
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_name}' not found")
    
    activity = activities[activity_name]
    spots_available = activity["max_participants"] - len(activity["participants"])
    
    return {
        "name": activity_name,
        "description": activity["description"],
        "schedule": activity["schedule"],
        "max_participants": activity["max_participants"],
        "current_participants": len(activity["participants"]),
        "spots_available": spots_available,
        "is_full": spots_available == 0
    }


@app.get("/activities/{activity_name}/participants")
def get_activity_participants(activity_name: str):
    """
    Get the list of participants signed up for a specific activity.
    
    Args:
        activity_name: Name of the activity
        
    Returns:
        Dictionary with participant count and list of participant emails
        
    Raises:
        HTTPException: 404 if activity is not found
    """
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_name}' not found")
    
    participants = activities[activity_name]["participants"]
    
    return {
        "activity": activity_name,
        "participant_count": len(participants),
        "participants": participants
    }


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str = Query(..., description="Student email address (must be @mergington.edu)")):
    """
    Sign up a student for an activity with comprehensive validation.
    
    This endpoint demonstrates GitHub Copilot's ability to:
    - Generate validation logic
    - Handle error cases
    - Provide clear error messages
    
    Args:
        activity_name: Name of the activity to sign up for
        email: Student's email address (must be from mergington.edu domain)
        
    Returns:
        Success message with confirmation details
        
    Raises:
        HTTPException: 400 for validation errors, 404 if activity not found
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_name}' not found")

    # Validate email format and domain
    if not is_valid_email(email):
        raise HTTPException(
            status_code=400,
            detail="Invalid email format. Email must be from @mergington.edu domain"
        )

    # Check if already signed up
    if is_already_signed_up(activity_name, email):
        raise HTTPException(
            status_code=400,
            detail=f"Student {email} is already signed up for {activity_name}"
        )

    # Check activity availability
    if not check_activity_availability(activity_name):
        raise HTTPException(
            status_code=400,
            detail=f"Activity '{activity_name}' is full. No spots available."
        )

    # Get the specific activity
    activity = activities[activity_name]

    # Add student to activity
    activity["participants"].append(email)
    
    spots_left = activity["max_participants"] - len(activity["participants"])
    
    return {
        "message": f"Successfully signed up {email} for {activity_name}",
        "activity": activity_name,
        "email": email,
        "spots_remaining": spots_left
    }


@app.delete("/activities/{activity_name}/signup")
def remove_signup(activity_name: str, email: str = Query(..., description="Student email address to remove")):
    """
    Remove a student's signup from an activity.
    
    Args:
        activity_name: Name of the activity
        email: Student's email address to remove
        
    Returns:
        Success message confirming removal
        
    Raises:
        HTTPException: 400 if student is not signed up, 404 if activity not found
    """
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail=f"Activity '{activity_name}' not found")
    
    # Check if student is signed up
    if not is_already_signed_up(activity_name, email):
        raise HTTPException(
            status_code=400,
            detail=f"Student {email} is not signed up for {activity_name}"
        )
    
    # Remove student from activity
    activities[activity_name]["participants"].remove(email)
    
    return {
        "message": f"Successfully removed {email} from {activity_name}",
        "activity": activity_name,
        "email": email
    }


# Main entry point for running the application
if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI application with hot reload enabled for development
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
