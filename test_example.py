"""Example usage of the test case generator"""
import json
from api_parser import APICollectionParser
from llm_service import LLMService
from models import APIEndpoint

# Example OpenAPI specification
EXAMPLE_OPENAPI = {
    "openapi": "3.0.0",
    "info": {"title": "User API", "version": "1.0.0"},
    "paths": {
        "/users": {
            "post": {
                "summary": "Create a new user",
                "description": "Create a new user with email and password",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "format": "email"},
                                    "password": {"type": "string", "minLength": 8},
                                    "name": {"type": "string"}
                                },
                                "required": ["email", "password"]
                            }
                        }
                    }
                },
                "responses": {
                    "201": {"description": "User created successfully"},
                    "400": {"description": "Invalid input"},
                    "409": {"description": "User already exists"}
                }
            }
        },
        "/users/{id}": {
            "get": {
                "summary": "Get user by ID",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "schema": {"type": "string"}
                    }
                ],
                "responses": {
                    "200": {"description": "User found"},
                    "404": {"description": "User not found"}
                }
            }
        }
    }
}

if __name__ == "__main__":
    # Parse API collection
    parser = APICollectionParser()
    endpoints = parser.parse_openapi(EXAMPLE_OPENAPI)
    
    print(f"Found {len(endpoints)} endpoints\n")
    
    # Generate test cases using LLM
    llm_service = LLMService()
    
    for endpoint in endpoints:
        print(f"\n{'='*60}")
        print(f"Generating test cases for: {endpoint.method} {endpoint.path}")
        print(f"{'='*60}")
        
        try:
            test_cases = llm_service.generate_test_cases(
                endpoint=endpoint,
                num_test_cases=3,
                test_types=["positive", "negative"]
            )
            
            for tc in test_cases:
                print(f"\nTest: {tc.name}")
                print(f"Type: {tc.test_type}")
                print(f"Expected Status: {tc.expected_status}")
                print(f"Payload: {json.dumps(tc.request_payload, indent=2)}")
                print(f"Assertions: {tc.assertions}")
        
        except Exception as e:
            print(f"Error generating test cases: {e}")