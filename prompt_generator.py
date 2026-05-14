from typing import List, Dict, Any
from models import APIEndpoint
import json

class PromptGenerator:
    """Generate LLM prompts for test case generation"""
    
    @staticmethod
    def generate_test_case_prompt(
        endpoint: APIEndpoint,
        num_test_cases: int = 5,
        test_types: List[str] = None
    ) -> str:
        """Generate a prompt for the LLM to create test cases"""
        
        if test_types is None:
            test_types = ["positive", "negative", "security"]
        
        request_body_schema = json.dumps(endpoint.request_body, indent=2) if endpoint.request_body else "None"
        
        prompt = f"""You are an expert QA engineer. Generate comprehensive test cases for the following API endpoint:

**Endpoint Details:**
- Method: {endpoint.method}
- Path: {endpoint.path}
- Summary: {endpoint.summary or 'N/A'}
- Description: {endpoint.description or 'N/A'}

**Request Body Schema:**
{request_body_schema}

**Parameters:**
{json.dumps(endpoint.parameters, indent=2) if endpoint.parameters else 'None'}

**Responses:**
{json.dumps(endpoint.responses, indent=2) if endpoint.responses else 'N/A'}

**Test Types to Generate:** {', '.join(test_types)}

Please generate {num_test_cases} diverse test cases in JSON format with the following structure for each test case:

{{
  "id": "TEST_001",
  "name": "Test case name",
  "description": "Detailed description",
  "test_type": "positive|negative|security|boundary",
  "request_payload": {{}},
  "request_headers": {{}},
  "expected_status": 200,
  "expected_response": {{}},
  "assertions": ["assertion1", "assertion2"]
}}

Guidelines:
1. **Positive tests**: Valid inputs, expected to succeed
2. **Negative tests**: Invalid inputs, edge cases, missing fields
3. **Security tests**: Authentication, authorization, injection attacks
4. **Boundary tests**: Min/max values, null, empty strings

Generate realistic, specific test cases with actual example values. Return ONLY valid JSON array, no markdown.
"""
        return prompt

    @staticmethod
    def generate_batch_prompt(
        endpoints: List[APIEndpoint],
        num_test_cases_per_endpoint: int = 3
    ) -> str:
        """Generate a prompt for multiple endpoints"""
        
        endpoints_description = "\n\n".join([
            f"Endpoint {i+1}:\n"
            f"- Method: {ep.method}\n"
            f"- Path: {ep.path}\n"
            f"- Summary: {ep.summary or 'N/A'}\n"
            f"- Request Body: {json.dumps(ep.request_body, indent=2) if ep.request_body else 'None'}"
            for i, ep in enumerate(endpoints[:10])  # Limit to 10 endpoints
        ])
        
        prompt = f"""You are an expert QA engineer. Generate comprehensive test cases for these API endpoints:

{endpoints_description}

Generate {num_test_cases_per_endpoint} test cases per endpoint in JSON format.

Return a JSON object with structure:
{{
  "endpoints": [
    {{
      "endpoint_path": "/path",
      "test_cases": [...]
    }}
  ]
}}

Create realistic test cases covering positive, negative, and security scenarios.
"""
        return prompt