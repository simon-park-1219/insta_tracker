# InstaTracker - Development Guidelines

## Project Overview
Instagram Follower/Following Tracker MVP. Monitors Instagram accounts for follower/following changes and notifies users.

## Tech Stack
- **Backend**: Python 3.11+ / FastAPI / SQLAlchemy / SQLite / APScheduler
- **Frontend**: Next.js 16 (App Router) / TypeScript / Tailwind CSS
- **Auth**: JWT (python-jose) + bcrypt

## Architecture
```
Frontend (Next.js :3000) → Backend API (FastAPI :8000) → SQLite
                                    ↓
                            APScheduler (periodic snapshots)
                                    ↓
                            Scraper (Mock or Instaloader)
                                    ↓
                            Diff Engine → Notifications
```

## Key Conventions

### Backend
- All models in `backend/app/models/` using SQLAlchemy 2.0 mapped_column style
- Pydantic schemas in `backend/app/schemas/` for request/response validation
- Services in `backend/app/services/` contain business logic (not routers)
- Scraper uses abstract interface (`base.py`) — always code against the interface
- Use `datetime.utcnow()` for all timestamps
- UUID strings (not integers) for all primary keys
- Tests in `backend/tests/` using pytest with in-memory SQLite

### Frontend
- Pages are client components ("use client") for interactive features
- API calls go through `src/lib/api.ts` — never call fetch directly in components
- Auth token stored in localStorage via `src/lib/auth.ts`
- All pages include `<Header />` for consistent navigation
- Use Tailwind classes — no CSS modules or styled-components

### Design System
- Primary: `#6366F1` (Indigo) — main actions
- Success: `#22C55E` (Green) — new followers
- Danger: `#EF4444` (Red) — lost followers
- Info: `#3B82F6` (Blue) — new following
- Warning: `#F59E0B` (Amber) — warnings

## Commands

### Backend
```bash
cd backend
pip install -r requirements.txt  # or install deps from pyproject.toml
python -m uvicorn app.main:app --reload --port 8000
python -m pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm install
npm run dev   # starts on :3000
npm run build
```

### Docker
```bash
docker-compose up --build
```

## API Docs
Backend auto-generates OpenAPI docs at `http://localhost:8000/docs`

## Environment Variables
See `.env.example` for all configuration options.
Key: `SCRAPER_MODE=mock` for development, `SCRAPER_MODE=instaloader` for production.
