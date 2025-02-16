from fastapi import FastAPI, HTTPException
import logging
from typing import List, Optional
from app.config import get_es_client
from app.schemas import Job, Candidate, MatchResponse
from app.services import get_document_by_id, find_matching_entities, validate_filters

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()
es = get_es_client()


@app.get("/jobs/{id}", response_model=Job)
def get_job(id: int):
    """Retrieve a job by ID from Elasticsearch."""
    job = get_document_by_id("jobs", id)
    print("Found document ", job)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


@app.get("/candidates/{id}", response_model=Candidate)
def get_candidate(id: str):
    """Retrieve a candidate by ID from Elasticsearch."""
    candidate = get_document_by_id("candidates", id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")
    return candidate


@app.get("/jobs/{id}/search-candidates", response_model=List[MatchResponse])
def find_matching_candidates(id: str, filters: Optional[str] = ""):
    """Find matching candidates for a given job ID based on filters."""
    job = get_document_by_id("jobs", id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    filter_list = filters.split(",") if filters else []

    # Validate filters
    validate_filters(filter_list)
    return find_matching_entities("candidates", job, filter_list)


@app.get("/candidates/{id}/search-jobs", response_model=List[MatchResponse])
def find_matching_jobs(id: str, filters: Optional[str] = ""):
    """Find matching jobs for a given candidate ID based on filters."""
    candidate = get_document_by_id("candidates", id)
    if not candidate:
        raise HTTPException(status_code=404, detail="Candidate not found")

    filter_list = filters.split(",") if filters else []

    # Validate filters
    validate_filters(filter_list)
    return find_matching_entities("jobs", candidate, filter_list)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True, host="0.0.0.0", port=8000)
