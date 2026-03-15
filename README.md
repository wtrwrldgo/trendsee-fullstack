# Trendsee Fullstack Test Assignment

This repository contains the completed test assignment for the Trendsee "vibe coder" full-stack role.

## Architecture & Technology Stack
- **Backend**: FastAPI
  - Async PostgreSQL (via `asyncpg`, without SQLAlchemy for raw parameterized speed)
  - Redis cache (via `redis-py` async)
  - JWT Authentication (PyJWT)
  - Strict Dependency Injection architecture
- **Frontend**: Vue.js 3 + Vite
  - Tailwind CSS (Pixel-perfect matching Figma layout)
  - Axios API Client
  - VueUse (`useIntersectionObserver` for infinite scroll logic)
- **Infrastructure**: Docker Compose (4 services tied together)

## Features Realized
- **Backend Caching Logic**: 
  - Hot posts (< 10 mins) are stored and fetched instantly from Redis.
  - Older posts are fetched from PostgreSQL with an artificial 2-second simulated delay (`asyncio.sleep(2)`).
- **Infinite Scroll Feed**: Frontend implements infinite scrolling triggering 500px before the bottom of the page.
- **Pixel-perfect Design**: `PostCard` and `AnalysisModal` styled precisely according to the provided Figma layout, including animations (`<Transition>`).
- **Security**: Parameterized queries to prevent SQL injections. JWT Bearer auth implementation.

## How to Run

1. Clone or navigate to the project root directory.
2. Build and start the containers using Docker Compose:

   ```bash
   docker-compose up --build
   ```

3. Services will be available at:
   - **Frontend**: http://localhost:5173
   - **Backend API**: http://localhost:8000
   - **PostgreSQL**: localhost:5432
   - **Redis**: localhost:6379

The database automatically initializes a `Test User` (ID = 1) and 15 mock posts so that the frontend pagination and caching can be tested immediately upon startup.

## Testing the API
A Postman collection is included in the repository root: `postman_collection.json`. Import it into Postman or Insomnia to explore the API.

Alternatively, you can access the automatically generated interactive API docs provided by FastAPI at http://localhost:8000/docs.
