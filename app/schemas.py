from typing import List, Optional
from pydantic import BaseModel


class Candidate(BaseModel):
    id: int
    top_skills: List[str]
    other_skills: List[str]
    seniority: str
    salary_expectation: float


class Job(BaseModel):
    id: int
    top_skills: List[str]
    other_skills: List[str]
    seniorities: List[str]
    max_salary: float


class MatchQueryParams(BaseModel):
    filters: List[str]


class MatchResponse(BaseModel):
    id: str
    relevance_score: float
