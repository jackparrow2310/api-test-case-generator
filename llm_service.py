from openai import OpenAI
from typing import List, Dict, Any, Optional
import json
from config import settings
from models import APIEndpoint, TestCase
from prompt_generator import PromptGenerator
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LLMService:
    """Service to interact with LLM for test case generation"""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model
    
    def generate_test_cases(
        self,
        endpoint: APIEndpoint,
        num_test_cases: int = 5,
        test_types: List[str] = None
    ) -> List[TestCase]:
        """Generate test cases for a single endpoint"""
        
        if test_types is None:
            test_types = ["positive", "negative", "security"]
        
        prompt = PromptGenerator.generate_test_case_prompt(
            endpoint=endpoint,
            num_test_cases=num_test_cases,
            test_types=test_types
        )
        
        logger.info(f"Generating test cases for {endpoint.method} {endpoint.path}")
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert QA engineer specializing in API testing. Always return valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=settings.temperature,
                max_tokens=4000
            )
            
            content = response.choices[0].message.content
            logger.info(f"LLM Response: {content[:200]}...")
            
            # Parse JSON response
            test_cases_data = self._parse_json_response(content)
            
            # Convert to TestCase objects
            test_cases = []
            for i, tc_data in enumerate(test_cases_data):
                test_case = TestCase(
                    id=tc_data.get("id", f"TEST_{i+1:03d}"),
                    name=tc_data.get("name", f"Test Case {i+1}"),
                    description=tc_data.get("description", ""),
                    method=endpoint.method,
                    endpoint=endpoint.path,
                    test_type=tc_data.get("test_type", "positive"),
                    request_payload=tc_data.get("request_payload"),
                    request_headers=tc_data.get("request_headers"),
                    expected_status=tc_data.get("expected_status", 200),
                    expected_response=tc_data.get("expected_response"),
                    assertions=tc_data.get("assertions", [])
                )
                test_cases.append(test_case)
            
            return test_cases
        
        except Exception as e:
            logger.error(f"Error generating test cases: {str(e)}")
            raise
    
    def _parse_json_response(self, content: str) -> List[Dict[str, Any]]:
        """Parse JSON from LLM response"""
        try:
            # Try direct parsing
            return json.loads(content)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown code blocks
            import re
            json_match = re.search(r'```json\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            json_match = re.search(r'```\n(.*?)\n```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            
            # Try to find JSON array
            json_match = re.search(r'\[.*\]', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
            
            raise ValueError("Could not parse JSON from LLM response")