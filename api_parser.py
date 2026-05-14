import json
import yaml
from typing import Dict, Any, List
from models import APIEndpoint

class APICollectionParser:
    """Parse API collections in various formats"""
    
    @staticmethod
    def parse_openapi(spec: Dict[str, Any]) -> List[APIEndpoint]:
        """Parse OpenAPI/Swagger specification"""
        endpoints = []
        
        paths = spec.get("paths", {})
        for path, methods in paths.items():
            for method, details in methods.items():
                if method.lower() not in ["get", "post", "put", "delete", "patch", "options", "head"]:
                    continue
                
                endpoint = APIEndpoint(
                    method=method.upper(),
                    path=path,
                    summary=details.get("summary"),
                    description=details.get("description"),
                    parameters=details.get("parameters"),
                    request_body=details.get("requestBody"),
                    responses=details.get("responses"),
                    tags=details.get("tags"),
                    security=details.get("security")
                )
                endpoints.append(endpoint)
        
        return endpoints
    
    @staticmethod
    def parse_postman(collection: Dict[str, Any]) -> List[APIEndpoint]:
        """Parse Postman collection"""
        endpoints = []
        
        def extract_endpoints(items: List[Dict[str, Any]], parent_path: str = ""):
            for item in items:
                if "request" in item:
                    request = item["request"]
                    url = request.get("url", {})
                    
                    if isinstance(url, str):
                        path = url
                    else:
                        path = "/".join(url.get("path", []))
                    
                    endpoint = APIEndpoint(
                        method=request.get("method", "GET").upper(),
                        path=path,
                        summary=item.get("name"),
                        parameters=request.get("header"),
                        request_body=request.get("body")
                    )
                    endpoints.append(endpoint)
                
                if "item" in item:
                    extract_endpoints(item["item"], parent_path)
        
        items = collection.get("item", [])
        extract_endpoints(items)
        
        return endpoints
    
    @staticmethod
    def parse_collection(collection_data: Dict[str, Any]) -> List[APIEndpoint]:
        """Auto-detect and parse API collection"""
        # Detect collection type
        if "openapi" in collection_data or "swagger" in collection_data:
            return APICollectionParser.parse_openapi(collection_data)
        elif "item" in collection_data:  # Postman
            return APICollectionParser.parse_postman(collection_data)
        else:
            raise ValueError("Unsupported API collection format")