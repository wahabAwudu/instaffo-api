from elasticsearch import Elasticsearch
from typing import Dict, List, Optional
from fastapi import HTTPException
from app.config import get_es_client

REQUIRED_FILTERS = {"salary_match", "top_skill_match", "seniority_match"}

# Initialize Elasticsearch client
es = get_es_client()

def get_document_by_id(index: str, doc_id: int) -> Optional[Dict]:
    """
    Retrieve a document from the specified Elasticsearch index by its ID.

    Args:
        index (str): The name of the Elasticsearch index (e.g., "jobs" or "candidates").
        doc_id (int): The ID of the document to retrieve.

    Returns:
        Optional[Dict]: The retrieved document or None if not found.
    """
    try:
        response = es.get(index=index, id=doc_id)
        doc_data = response["_source"]
        doc_data["id"] = response["_id"]
        return doc_data
    except Exception as e:
        print(f"Error retrieving document from {index}: {e}")
        return None


def build_query(target_doc: Dict, filters: List[str]) -> Dict:
    """
    Constructs an Elasticsearch query based on the given target document and filters.

    Args:
        target_doc (Dict): The job or candidate document used as the basis for matching.
        filters (List[str]): List of filters to apply (e.g., ["salary_match", "top_skill_match", "seniority_match"]).

    Returns:
        Dict: The Elasticsearch query dictionary.
    """
    should_clauses = []

    if "salary_match" in filters:
        if "salary_expectation" in target_doc:  # Candidate -> Match jobs with max_salary >= salary_expectation
            should_clauses.append({"range": {"max_salary": {"gte": target_doc["salary_expectation"]}}})
        if "max_salary" in target_doc:  # Job -> Match candidates with salary_expectation <= max_salary
            should_clauses.append({"range": {"salary_expectation": {"lte": target_doc["max_salary"]}}})

    if "top_skill_match" in filters and "top_skills" in target_doc:
        min_match = min(len(target_doc["top_skills"]), 2)  # At least 2 skills must match
        should_clauses.append({
            "terms_set": {
                "top_skills": {
                    "terms": target_doc["top_skills"],
                    "minimum_should_match_script": {
                        "source": "Math.max(doc['top_skills'].size(), params.num_terms)",
                        "params": {"num_terms": min_match}
                    }
                }
            }
        })

    if "seniority_match" in filters:
        if "seniority" in target_doc:  # Candidate -> Match jobs with same seniority
            should_clauses.append({"terms": {"seniorities": [target_doc["seniority"]]}})
        if "seniorities" in target_doc:  # Job -> Match candidates with matching seniority
            should_clauses.append({"terms": {"seniority": target_doc["seniorities"]}})

    return {"query": {"bool": {"should": should_clauses}}} if should_clauses else {"match_all": {}}


def find_matching_entities(index: str, target_doc: Dict, filters: List[str]) -> List[Dict]:
    """
    Finds matching documents in Elasticsearch based on the given target document and filters.

    Args:
        index (str): The Elasticsearch index to search in (either "jobs" or "candidates").
        target_doc (Dict): The job or candidate document used for matching.
        filters (List[str]): List of filters to apply.

    Returns:
        List[Dict]: List of matching documents with their IDs and relevance scores.
    """
    query = build_query(target_doc, filters)
    
    response = es.search(index=index, body=query)
    results = [
        {"id": hit["_id"], "relevance_score": hit["_score"]}
        for hit in response["hits"]["hits"]
    ]
    return results


def validate_filters(filters: List[str]):
    """Ensures at least two valid filters are provided."""
    if len(filters) < 2:
        raise HTTPException(
            status_code=400,
            detail=f"At least two filters are required. Allowed filters: {', '.join(REQUIRED_FILTERS)}"
        )

    invalid_filters = [f for f in filters if f not in REQUIRED_FILTERS]
    if invalid_filters:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid filters provided: {', '.join(invalid_filters)}. Allowed filters: {', '.join(REQUIRED_FILTERS)}"
        )
