from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class APIEndpoint(BaseModel):
    """Represents an API endpoint"""
    method: str
    path: str
    summary: Optional[str] = None
    description: Optional[str] = None
    parameters: Optional[List[Dict[str, Any]]] = None
    request_body: Optional[Dict[str, Any]] = None
    responses: Optional[Dict[str, Any]] = None
    tags: Optional[List[str]] = None
    security: Optional[List[Dict[str, Any]]] = None

class TestCase(BaseModel):
    """Represents a generated test case"""
    id: str
    name: str
    description: str
    method: str
    endpoint: str
    test_type: str  # positive, negative, security, boundary
    request_payload: Optional[Dict[str, Any]] = None
    request_headers: Optional[Dict[str, str]] = None
    expected_status: int
    expected_response: Optional[Dict[str, Any]] = None
    assertions: List[str]

class TestCaseGenerationRequest(BaseModel):
    """Request to generate test cases"""
    api_collection: Dict[str, Any]
    num_test_cases: int = 5
    test_types: List[str] = ["positive", "negative", "security"]

class TestCaseGenerationResponse(BaseModel):
    """Response with generated test cases"""
    endpoint: str
    test_cases: List[TestCase]
    total_generated: int