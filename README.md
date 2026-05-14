# API Test Case Generator with LLM

An intelligent tool that uses Large Language Models (LLM) to automatically generate comprehensive test cases from API collections (OpenAPI, Swagger, Postman).

## 🚀 Features

- **Multi-format Support**: OpenAPI/Swagger, Postman Collections
- **Diverse Test Generation**: Positive, negative, security, and boundary test cases
- **LLM Integration**: Uses OpenAI GPT-4 for intelligent test generation
- **RESTful API**: FastAPI-based web service
- **Docker Support**: Easy deployment with Docker Compose
- **Batch Processing**: Generate test cases for multiple endpoints

## 📋 Requirements

- Python 3.8+
- OpenAI API key
- FastAPI, Pydantic, OpenAI SDK

## 🔧 Installation

### 1. Clone Repository
```bash
git clone https://github.com/jackparrow2310/api-test-case-generator.git
cd api-test-case-generator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
export OPENAI_API_KEY="sk-..."
```

## ▶️ Running the Application

### Local Development
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### Using Docker
```bash
docker-compose up --build
```

## 📡 API Endpoints

### 1. Health Check
```bash
GET /health
```

### 2. Generate Test Cases from Collection
```bash
POST /generate-test-cases
Content-Type: application/json

{
  "api_collection": {
    "openapi": "3.0.0",
    "paths": {...}
  },
  "num_test_cases": 5,
  "test_types": ["positive", "negative", "security"]
}
```

### 3. Upload API Collection File
```bash
POST /upload-collection
Content-Type: multipart/form-data

file: collection.json (or .yaml)
```

### 4. Generate for Specific Endpoint
```bash
POST /generate/users?method=POST&num_test_cases=5
```

### 5. List API Endpoints
```bash
GET /endpoints
```

## 💡 Example Usage

### Using Python
```python
from api_parser import APICollectionParser
from llm_service import LLMService
from models import APIEndpoint

# Create an endpoint
endpoint = APIEndpoint(
    method="POST",
    path="/users",
    summary="Create user",
    request_body={"email": "string", "password": "string"}
)

# Generate test cases
llm_service = LLMService()
test_cases = llm_service.generate_test_cases(endpoint, num_test_cases=5)

for tc in test_cases:
    print(f"{tc.name}: {tc.description}")
```

### Using cURL
```bash
curl -X POST http://localhost:8000/generate/users \
  -H "Content-Type: application/json" \
  -d '{
    "method": "POST",
    "num_test_cases": 3
  }'
```

## 📊 Test Case Types

### Positive Tests
- Valid inputs expected to succeed
- Happy path scenarios
- Standard workflows

### Negative Tests
- Invalid inputs
- Missing required fields
- Boundary conditions
- Wrong data types

### Security Tests
- Authentication failures
- Authorization violations
- Injection attacks
- CORS issues

## 🏗️ Architecture

```
┌─────────────────────────────────┐
│   API Collection (JSON/YAML)    │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   API Collection Parser         │
│  (OpenAPI/Postman Support)      │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Prompt Generator              │
│  (Structured Prompt Creation)   │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   LLM Service (OpenAI GPT-4)    │
│  (Test Case Generation)         │
└────────────┬────────────────────┘
             │
             ▼
┌─────────────────────────────────┐
│   Test Cases Output             │
│  (JSON Format)                  │
└─────────────────────────────────┘
```

## 🧪 Running Tests

```bash
python test_example.py
```

## 📝 Sample Output

```json
{
  "status": "success",
  "total_endpoints": 2,
  "total_test_cases": 6,
  "test_cases": [
    {
      "id": "TEST_001",
      "name": "Create user with valid data",
      "description": "Verify user creation with all required fields",
      "method": "POST",
      "endpoint": "/users",
      "test_type": "positive",
      "request_payload": {
        "email": "john@example.com",
        "password": "SecurePass123"
      },
      "expected_status": 201,
      "assertions": [
        "response.status_code == 201",
        "response.json.id exists",
        "response.json.email == 'john@example.com'"
      ]
    }
  ]
}
```

## ⚙️ Configuration

Edit `.env` to customize:

- `OPENAI_API_KEY`: Your OpenAI API key
- `OPENAI_MODEL`: Model to use (gpt-4o, gpt-4-turbo, etc.)
- `MAX_TEST_CASES`: Maximum test cases to generate
- `TEMPERATURE`: LLM temperature (0.0-2.0)

## 🔒 Security Considerations

- Store API keys securely (use environment variables)
- Don't commit .env file to version control
- Use HTTPS in production
- Validate user inputs
- Rate limit API calls

## 🚀 Deployment

### Using Heroku
```bash
heroku create your-app-name
heroku config:set OPENAI_API_KEY=sk-...
git push heroku main
```

### Using AWS EC2
```bash
# SSH into instance
# Install Python, pip, requirements
# Configure environment
# Run: python main.py
```

## 📚 Dependencies

- **FastAPI**: Modern web framework
- **Pydantic**: Data validation
- **OpenAI**: LLM API client
- **LangChain**: LLM orchestration
- **PyYAML**: YAML parsing

## 🐛 Troubleshooting

### OpenAI API Error
- Verify API key is correct
- Check API key has sufficient credits
- Ensure API key permissions are set correctly

### JSON Parsing Error
- Ensure API collection is valid JSON/YAML
- Check collection format is supported

### Slow Response
- Reduce num_test_cases
- Use faster model (gpt-3.5-turbo)
- Check OpenAI API status

## 📖 Documentation

For more information, visit:
- [OpenAI API Docs](https://platform.openai.com/docs)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [OpenAPI Spec](https://spec.openapis.org/)

## 📄 License

MIT License - feel free to use and modify

## 👥 Contributing

Contributions are welcome! Please submit pull requests or open issues for bugs and feature requests.

## 📧 Support

For issues and questions, please open a GitHub issue or contact the maintainer.