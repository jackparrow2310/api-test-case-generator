from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from typing import List
import json
import yaml
import logging
from api_parser import APICollectionParser
from llm_service import LLMService
from models import TestCaseGenerationRequest, TestCaseGenerationResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="API Test Case Generator",
    description="Generate test cases from API collections using LLM",
    version="1.0.0"
)

llm_service = LLMService()
api_parser = APICollectionParser()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "API Test Case Generator"}

@app.post("/generate-test-cases")
async def generate_test_cases(request: TestCaseGenerationRequest):
    """Generate test cases from API collection"""
    try:
        # Parse API collection
        endpoints = api_parser.parse_collection(request.api_collection)
        logger.info(f"Parsed {len(endpoints)} endpoints")
        
        if not endpoints:
            raise HTTPException(status_code=400, detail="No valid endpoints found in collection")
        
        # Generate test cases for each endpoint
        all_test_cases = []
        for endpoint in endpoints[:5]:  # Limit to 5 endpoints for demo
            test_cases = llm_service.generate_test_cases(
                endpoint=endpoint,
                num_test_cases=request.num_test_cases,
                test_types=request.test_types
            )
            all_test_cases.extend(test_cases)
        
        return {
            "status": "success",
            "total_endpoints": len(endpoints),
            "total_test_cases": len(all_test_cases),
            "test_cases": all_test_cases
        }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/upload-collection")
async def upload_collection(file: UploadFile = File(...)):
    """Upload and parse API collection file"""
    try:
        content = await file.read()
        
        # Determine file type and parse
        if file.filename.endswith('.json'):
            collection_data = json.loads(content)
        elif file.filename.endswith(('.yaml', '.yml')):
            collection_data = yaml.safe_load(content)
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Use JSON or YAML.")
        
        # Parse endpoints
        endpoints = api_parser.parse_collection(collection_data)
        
        return {
            "status": "success",
            "filename": file.filename,
            "endpoints_found": len(endpoints),
            "endpoints": [
                {
                    "method": ep.method,
                    "path": ep.path,
                    "summary": ep.summary
                }
                for ep in endpoints
            ]
        }
    
    except Exception as e:
        logger.error(f"Error uploading collection: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/{endpoint_path:path}")
async def generate_for_endpoint(
    endpoint_path: str,
    method: str = "GET",
    num_test_cases: int = 5
):
    """Generate test cases for a specific endpoint"""
    try:
        from models import APIEndpoint
        
        endpoint = APIEndpoint(
            method=method.upper(),
            path=f"/{endpoint_path}",
            summary=f"{method} {endpoint_path}"
        )
        
        test_cases = llm_service.generate_test_cases(
            endpoint=endpoint,
            num_test_cases=num_test_cases
        )
        
        return {
            "status": "success",
            "endpoint": endpoint_path,
            "method": method,
            "test_cases_generated": len(test_cases),
            "test_cases": test_cases
        }
    
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/endpoints")
async def list_endpoints():
    """List all available API endpoints"""
    return {
        "endpoints": [
            {"method": "POST", "path": "/generate-test-cases", "description": "Generate test cases from API collection"},
            {"method": "POST", "path": "/upload-collection", "description": "Upload API collection file"},
            {"method": "POST", "path": "/generate/{endpoint_path}", "description": "Generate test cases for specific endpoint"},
            {"method": "GET", "path": "/health", "description": "Health check"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)