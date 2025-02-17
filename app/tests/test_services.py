import pytest
from app.services import validate_filters
from fastapi import HTTPException


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
