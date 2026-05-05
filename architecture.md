# Architecture

## System Context (C4 Level 1)
User -> Todo API (FastAPI) -> PostgreSQL

## Container Diagram (C4 Level 2)

### Containers
- **API Application** (Python FastAPI):
  - Handles HTTP requests
  - Validates input with Pydantic
  - Authenticates via JWT
  - Business logic in services
- **Database** (PostgreSQL):
  - Stores users and tasks

### Components inside API Application
- **auth module**: Registration, login, JWT creation/validation
- **tasks module**: CRUD operations for tasks, ownership checks
- **core module**: Config, DB session, error handlers
- **db module**: SQLAlchemy models, migrations (Alembic)

### Data Flow
1. User sends request -> FastAPI route
2. Route delegates to service layer
3. Service uses repository pattern to interact with DB
4. Response returned

### Technology Stack
- Python 3.10+
- FastAPI
- SQLAlchemy (async or sync, default sync for simplicity)
- Alembic for migrations
- PyJWT / python-jose for JWT
- passlib[bcrypt] for password hashing

### Security
- Passwords hashed with bcrypt
- JWT access token (expiry configurable)
- All endpoints except /auth/register and /auth/login require Bearer token
- Ownership enforced: each task is tied to user_id from token
