# Trendsee Test Task

Fullstack publication feed service: FastAPI + PostgreSQL + Redis + JWT backend, Vue 3 + TypeScript frontend.

## Quick Start

```bash
docker-compose up --build
```

- **Backend API**: http://localhost:8000
- **Frontend**: http://localhost:5173
- **API Docs**: http://localhost:8000/docs

## API Endpoints

### Users
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/users` | No | Create user, returns JWT |
| GET | `/users/{id}/token` | No | Get JWT by user ID |
| PATCH | `/users/{id}` | Yes | Update user name |
| DELETE | `/users/{id}` | Yes | Delete user |

### Publications
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/publications` | Yes | Create publication |
| GET | `/publications/user/{id}` | No | Get user's publications (paginated) |
| PATCH | `/publications/{id}` | Yes | Update publication |
| DELETE | `/publications/{id}` | Yes | Delete publication |

### Instagram
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/instagram/reel/{reel_id}/stats` | No | Get real engagement stats for a reel |

## Caching

- Publications are cached in Redis with 600s TTL on creation
- Reading from cache is instant; cache miss triggers a 2s simulated delay before Postgres query
- Cache keys: `pub:{id}`, `user_pubs:{user_id}:{limit}:{offset}`
- On mutation, all paginated cache keys for the user are invalidated via SCAN pattern match

## Tech Stack

- **Backend**: FastAPI, asyncpg (raw queries, no ORM), Redis, PyJWT, httpx
- **Frontend**: Vue 3, TypeScript, Vite, Tailwind CSS, Vue Router, Axios, VueUse
- **Infrastructure**: Docker Compose, PostgreSQL 16, Redis 7

## Project Structure

```
backend/app/
├── main.py              # FastAPI app, CORS, startup
├── config.py            # Settings (DB, Redis, JWT)
├── db.py                # asyncpg connection pool
├── redis_client.py      # Redis connection
├── auth/                # JWT create/decode, get_current_user DI
├── api/
│   ├── auth.py          # Auth endpoints
│   ├── users.py         # Users CRUD
│   ├── publications.py  # Publications CRUD with Redis caching
│   └── instagram.py     # Instagram reel stats proxy
└── models/              # Pydantic v2 schemas

frontend/src/
├── api/index.ts         # Axios client with JWT interceptor
├── views/               # FeedView (infinite scroll feed)
├── components/          # PostCard, AnalysisModal, AnimatedNumber
├── composables/         # useLike, useInfiniteScroll
└── router/              # Vue Router config
```

## Postman

Import `backend/postman_collection.json` into Postman. Run "Create User" first to auto-set token and userId variables.
