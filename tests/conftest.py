import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Fixture providing a FastAPI TestClient"""
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Fixture to reset activities to default state before each test"""
    # Store original state
    original_activities = {
        name: {
            "description": activity["description"],
            "schedule": activity["schedule"],
            "max_participants": activity["max_participants"],
            "participants": activity["participants"].copy()
        }
        for name, activity in activities.items()
    }
    
    yield
    
    # Restore original state
    activities.clear()
    activities.update(original_activities)
