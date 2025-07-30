# FastAPI Microservice Template

A clean, production-ready FastAPI template for microservices with Docker support.

## Quick Start

1. **Clone and customize:**
    ```bash
    git clone <your-template-repo>
    cd fastapi-microservice-template
    # Update PROJECT_NAME in app/core/config.py
    ```

2. **Local Development:**
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    uvicorn app.main:app --reload
    ```

3. **Docker Development:**
    ```bash
    docker-compose up --build
    ```

4. **Access the API:**
    - API: [http://localhost:8000](http://localhost:8000)
    - Interactive docs: [http://localhost:8000/docs](http://localhost:8000/docs)
    - Health check: [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)

---

## Adding New Endpoints

1. Create a new file in `app/api/v1/endpoints/`.
2. Define your router and endpoints.
3. Add the router to `app/api/v1/router.py`.
4. Create any needed models in `app/models/`.

**Example:**

Create a new endpoint file:

```python
# app/api/v1/endpoints/users.py
from fastapi import APIRouter
from app.models.response import MessageResponse

router = APIRouter()

@router.get("/", response_model=MessageResponse)
async def get_users():
    return MessageResponse(message="Users endpoint")
```

Register the router in `router.py`:

```python
from app.api.v1.endpoints import users

api_router.include_router(users.router, prefix="/users", tags=["users"])
```