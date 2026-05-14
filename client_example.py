"""Example client to interact with the API Test Case Generator"""
import requests
import json
from typing import Dict, Any

class TestCaseGeneratorClient:
    """Client for API Test Case Generator"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def health_check(self) -> Dict[str, Any]:
        """Check if service is running"""
        response = requests.get(f"{self.base_url}/health")
        return response.json()
    
    def generate_from_collection(
        self,
        api_collection: Dict[str, Any],
        num_test_cases: int = 5,
        test_types: list = None
    ) -> Dict[str, Any]:
        """Generate test cases from API collection"""
        if test_types is None:
            test_types = ["positive", "negative", "security"]
        
        payload = {
            "api_collection": api_collection,
            "num_test_cases": num_test_cases,
            "test_types": test_types
        }
        
        response = requests.post(
            f"{self.base_url}/generate-test-cases",
            json=payload
        )
        return response.json()
    
    def upload_collection(self, file_path: str) -> Dict[str, Any]:
        """Upload API collection file"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            response = requests.post(
                f"{self.base_url}/upload-collection",
                files=files
            )
        return response.json()
    
    def generate_for_endpoint(
        self,
        endpoint_path: str,
        method: str = "GET",
        num_test_cases: int = 5
    ) -> Dict[str, Any]:
        """Generate test cases for specific endpoint"""
        params = {
            "method": method,
            "num_test_cases": num_test_cases
        }
        
        response = requests.post(
            f"{self.base_url}/generate/{endpoint_path}",
            params=params
        )
        return response.json()
    
    def list_endpoints(self) -> Dict[str, Any]:
        """Get list of all available endpoints"""
        response = requests.get(f"{self.base_url}/endpoints")
        return response.json()


if __name__ == "__main__":
    # Initialize client
    client = TestCaseGeneratorClient()
    
    # Check health
    print("Checking service health...")
    health = client.health_check()
    print(f"Health: {health}\n")
    
    # Example API collection
    example_collection = {
        "openapi": "3.0.0",
        "info": {"title": "Example API", "version": "1.0.0"},
        "paths": {
            "/posts": {
                "get": {
                    "summary": "List all posts",
                    "responses": {"200": {"description": "Success"}}
                },
                "post": {
                    "summary": "Create a post",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "title": {"type": "string"},
                                        "content": {"type": "string"}
                                    }
                                }
                            }
                        }
                    },
                    "responses": {"201": {"description": "Created"}}
                }
            }
        }
    }
    
    # Generate test cases
    print("Generating test cases...")
    result = client.generate_from_collection(
        api_collection=example_collection,
        num_test_cases=3,
        test_types=["positive", "negative"]
    )
    
    print(f"Generated {result['total_test_cases']} test cases")
    for tc in result['test_cases'][:2]:
        print(f"\n- {tc['name']}")
        print(f"  Type: {tc['test_type']}")
        print(f"  Status: {tc['expected_status']}")