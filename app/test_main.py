import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services import validate_filters
from fastapi import HTTPException

client = TestClient(app)


# ------------------------
# Testing Individual Endpoints
# ------------------------

def test_get_candidate_by_id():
    response = client.get("/candidates/123")
    assert response.status_code == 200
    assert "id" in response.json()


def test_get_job_by_id():
    response = client.get("/jobs/126")
    assert response.status_code == 200
    assert "id" in response.json()


def test_search_candidates_with_valid_filters():
    response = client.get("/jobs/126/search-candidates?filters=salary_match,top_skill_match")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_candidates_with_invalid_filters():
    response = client.get("/jobs/126/search-candidates?filters=invalid_filter,salary_match")
    assert response.status_code == 400
    assert "Invalid filters provided" in response.json()["detail"]


def test_search_candidates_with_insufficient_filters():
    response = client.get("/jobs/126/search-candidates?filters=salary_match")
    assert response.status_code == 400
    assert "At least two filters are required" in response.json()["detail"]


def test_search_jobs_with_valid_filters():
    response = client.get("/candidates/123/search-jobs?filters=top_skill_match,seniority_match")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_search_jobs_with_invalid_filters():
    response = client.get("/candidates/123/search-jobs?filters=invalid_filter,salary_match")
    assert response.status_code == 400
    assert "Invalid filters provided" in response.json()["detail"]


# ------------------------
# Testing the Filter Validator Function
# ------------------------

def test_validate_filters_valid():
    """Ensure valid filters pass without error."""
    try:
        validate_filters(["salary_match", "top_skill_match"])
    except HTTPException:
        pytest.fail("validate_filters() raised an exception unexpectedly.")


def test_validate_filters_too_few():
    """Ensure error is raised when less than two filters are passed."""
    with pytest.raises(HTTPException) as excinfo:
        validate_filters(["salary_match"])
    assert excinfo.value.status_code == 400
    assert "At least two filters are required" in excinfo.value.detail


def test_validate_filters_invalid():
    """Ensure error is raised when an invalid filter is included."""
    with pytest.raises(HTTPException) as excinfo:
        validate_filters(["salary_match", "invalid_filter"])
    assert excinfo.value.status_code == 400
    assert "Invalid filters provided" in excinfo.value.detail
