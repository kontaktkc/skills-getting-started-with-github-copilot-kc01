# Mergington High School Activities API

A FastAPI application that demonstrates GitHub Copilot capabilities through a real-world example: managing student extracurricular activities.

## 🎯 GitHub Copilot Demonstration

This project showcases various GitHub Copilot features including:
- Code generation and completion
- Comprehensive documentation generation
- Test case creation
- Input validation and error handling
- API endpoint design

**📖 See [COPILOT_EXAMPLES.md](../COPILOT_EXAMPLES.md) for detailed examples and [SUMMARY.md](../SUMMARY.md) for a complete overview.**

## Features

### Core Functionality
- View all available extracurricular activities
- Sign up for activities with validation
- View activity participants
- Remove signups
- Get detailed activity information

### Enhanced with Copilot
- ✅ Email validation (must be @mergington.edu domain)
- ✅ Duplicate signup prevention
- ✅ Activity capacity checking
- ✅ Comprehensive error handling
- ✅ Detailed API documentation
- ✅ 25 comprehensive tests (all passing!)

## Getting Started

1. Install the dependencies:

   ```bash
   pip install -r ../requirements.txt
   ```

2. Run the application:

   ```bash
   python app.py
   ```

3. Open your browser and go to:
   - Web Interface: http://localhost:8000/
   - API documentation: http://localhost:8000/docs
   - Alternative documentation: http://localhost:8000/redoc

## API Endpoints

| Method | Endpoint                                                          | Description                                                         |
| ------ | ----------------------------------------------------------------- | ------------------------------------------------------------------- |
| GET    | `/activities`                                                     | Get all activities with their details and current participant count |
| GET    | `/activities/{activity_name}`                                     | Get detailed information about a specific activity                  |
| GET    | `/activities/{activity_name}/participants`                        | Get the list of participants in an activity                         |
| POST   | `/activities/{activity_name}/signup?email=student@mergington.edu` | Sign up for an activity (with validation)                           |
| DELETE | `/activities/{activity_name}/signup?email=student@mergington.edu` | Remove a signup from an activity                                    |

## Testing

Run the comprehensive test suite:

```bash
pytest test_app.py -v
```

**All 25 tests pass!** The test suite covers:
- Email validation
- Activity availability checking
- API endpoint functionality
- Edge cases and error handling

## Data Model

The application uses a simple data model with meaningful identifiers:

1. **Activities** - Uses activity name as identifier:

   - Description
   - Schedule
   - Maximum number of participants allowed
   - List of student emails who are signed up

2. **Students** - Uses email as identifier (validation enforced):
   - Must be from @mergington.edu domain
   - Cannot sign up twice for the same activity

All data is stored in memory, which means data will be reset when the server restarts.

## Examples

### Using cURL

```bash
# Get all activities
curl http://localhost:8000/activities

# Sign up for Chess Club
curl -X POST "http://localhost:8000/activities/Chess%20Club/signup?email=john@mergington.edu"

# View participants
curl http://localhost:8000/activities/Chess%20Club/participants

# Remove signup
curl -X DELETE "http://localhost:8000/activities/Chess%20Club/signup?email=john@mergington.edu"
```

### Using Python

```python
import requests

# Get activities
response = requests.get("http://localhost:8000/activities")
print(response.json())

# Sign up
response = requests.post(
    "http://localhost:8000/activities/Chess Club/signup",
    params={"email": "student@mergington.edu"}
)
print(response.json())
```

See [COPILOT_EXAMPLES.md](../COPILOT_EXAMPLES.md) for more examples!

## What's New?

This enhanced version includes improvements generated with GitHub Copilot:
- 🔒 Input validation and security checks
- 📝 Comprehensive documentation
- 🧪 Full test coverage
- 🚀 Additional API endpoints
- ✨ Better error handling
- 📊 Detailed API responses

## Learn More

- [COPILOT_EXAMPLES.md](../COPILOT_EXAMPLES.md) - Detailed examples of Copilot capabilities
- [SUMMARY.md](../SUMMARY.md) - Complete project summary
- [test_app.py](test_app.py) - View the comprehensive test suite
