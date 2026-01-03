# GitHub Copilot Demonstration Examples

This document showcases what's possible with GitHub Copilot through practical examples from the Mergington High School Activities API project.

## Table of Contents
1. [Code Generation](#code-generation)
2. [Documentation Generation](#documentation-generation)
3. [Test Creation](#test-creation)
4. [Error Handling](#error-handling)
5. [Refactoring Assistance](#refactoring-assistance)
6. [API Usage Examples](#api-usage-examples)

---

## Code Generation

GitHub Copilot excels at generating boilerplate code and completing repetitive patterns.

### Example 1: Validation Functions

Copilot can generate validation functions based on comments or function signatures:

```python
def is_valid_email(email: str) -> bool:
    """Validate email format and domain"""
    # Copilot can suggest the regex pattern and validation logic
    email_pattern = r'^[a-zA-Z0-9._%+-]+@mergington\.edu$'
    return re.match(email_pattern, email) is not None
```

### Example 2: Helper Functions

When you start typing a function name, Copilot suggests the entire implementation:

```python
def check_activity_availability(activity_name: str) -> bool:
    """Check if activity has available spots"""
    # Copilot suggests checking participant count vs max participants
    if activity_name not in activities:
        return False
    
    activity = activities[activity_name]
    current_participants = len(activity["participants"])
    max_participants = activity["max_participants"]
    
    return current_participants < max_participants
```

---

## Documentation Generation

Copilot can automatically generate comprehensive docstrings and comments.

### Example: Detailed Docstrings

```python
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
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
```

---

## Test Creation

Copilot can generate comprehensive test cases based on your code.

### Example: Test Classes

When you write a test class name, Copilot suggests relevant test methods:

```python
class TestEmailValidation:
    """Test cases for email validation functionality"""
    
    def test_valid_mergington_email(self):
        """Test that valid mergington.edu emails are accepted"""
        assert is_valid_email("student@mergington.edu") is True
        assert is_valid_email("john.doe@mergington.edu") is True
    
    def test_invalid_domain(self):
        """Test that emails from other domains are rejected"""
        assert is_valid_email("student@gmail.com") is False
        assert is_valid_email("student@otherschool.edu") is False
```

### Example: Edge Case Tests

Copilot helps identify and test edge cases:

```python
def test_last_spot_in_activity(self):
    """Test signup when only one spot remains"""
    max_participants = activities["Chess Club"]["max_participants"]
    activities["Chess Club"]["participants"] = [
        f"student{i}@mergington.edu" for i in range(max_participants - 1)
    ]
    
    # This should succeed
    response = client.post("/activities/Chess Club/signup?email=lastone@mergington.edu")
    assert response.status_code == 200
    assert response.json()["spots_remaining"] == 0
```

---

## Error Handling

Copilot suggests appropriate error handling patterns.

### Example: Comprehensive Validation

```python
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
```

---

## Refactoring Assistance

Copilot helps refactor code for better maintainability.

### Before Refactoring:

```python
@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")
    
    activity = activities[activity_name]
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
```

### After Refactoring with Copilot:

```python
# Copilot suggests extracting validation logic into separate functions
def is_valid_email(email: str) -> bool:
    # Validation logic
    pass

def check_activity_availability(activity_name: str) -> bool:
    # Availability check logic
    pass

@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    # Use helper functions for validation
    # Copilot suggests comprehensive error handling
    pass
```

---

## API Usage Examples

### Using cURL

#### Get all activities:
```bash
curl http://localhost:8000/activities
```

#### Get specific activity details:
```bash
curl http://localhost:8000/activities/Chess%20Club
```

#### Get activity participants:
```bash
curl http://localhost:8000/activities/Chess%20Club/participants
```

#### Sign up for an activity:
```bash
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
```

#### Remove a signup:
```bash
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
```

### Using Python Requests

```python
import requests

base_url = "http://localhost:8000"

# Get all activities
response = requests.get(f"{base_url}/activities")
activities = response.json()
print(activities)

# Sign up for Chess Club
response = requests.post(
    f"{base_url}/activities/Chess Club/signup",
    params={"email": "student@mergington.edu"}
)
print(response.json())

# Get participants
response = requests.get(f"{base_url}/activities/Chess Club/participants")
participants = response.json()
print(f"Participants: {participants['participant_count']}")
```

### Using JavaScript Fetch

```javascript
// Get all activities
fetch('/activities')
  .then(response => response.json())
  .then(data => console.log(data));

// Sign up for an activity
fetch('/activities/Chess%20Club/signup?email=student@mergington.edu', {
  method: 'POST'
})
  .then(response => response.json())
  .then(data => console.log(data.message));

// Remove a signup
fetch('/activities/Chess%20Club/signup?email=student@mergington.edu', {
  method: 'DELETE'
})
  .then(response => response.json())
  .then(data => console.log(data.message));
```

---

## Key Takeaways

### What GitHub Copilot Helps With:

1. **Code Completion**: Suggests entire functions, classes, and code blocks
2. **Documentation**: Generates detailed docstrings and comments
3. **Testing**: Creates comprehensive test cases including edge cases
4. **Error Handling**: Suggests appropriate validation and error responses
5. **Refactoring**: Helps identify opportunities to improve code structure
6. **API Design**: Suggests RESTful patterns and best practices
7. **Type Hints**: Adds proper type annotations
8. **Consistency**: Maintains coding style throughout the project

### Best Practices When Using Copilot:

1. **Write Clear Comments**: Better comments lead to better suggestions
2. **Review Suggestions**: Always review and understand Copilot's suggestions
3. **Iterate**: Use Copilot's suggestions as a starting point and refine
4. **Test Thoroughly**: Verify that generated code works as expected
5. **Context Matters**: Provide good context through file structure and naming
6. **Security**: Always review security-sensitive code carefully

---

## Running the Application

1. Install dependencies:
   ```bash
   pip install fastapi uvicorn pytest httpx
   ```

2. Run the application:
   ```bash
   cd src
   python app.py
   ```

3. Run tests:
   ```bash
   cd src
   pytest test_app.py -v
   ```

4. View API documentation:
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc
   - Web Interface: http://localhost:8000/

---

## Conclusion

GitHub Copilot is a powerful AI pair programmer that can significantly accelerate development by:
- Reducing boilerplate code writing
- Suggesting best practices and patterns
- Helping with documentation
- Generating comprehensive tests
- Assisting with refactoring

Remember that Copilot is a tool to enhance your productivity, not replace your judgment. Always review, test, and understand the code it suggests.
