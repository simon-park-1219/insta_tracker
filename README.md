# InstaTracker

Instagram Follower/Following Tracker MVP - Track changes in Instagram followers and following, and get notified when changes occur.

## Features

- **Account Tracking**: Add Instagram accounts to monitor
- **Automated Snapshots**: Periodic snapshots of followers/following lists
- **Change Detection**: Detects new followers, lost followers, new following, unfollowing
- **Notifications**: In-app and email notifications when changes are detected
- **Dashboard**: Visual overview with summary cards and follower trend charts
- **Account Detail**: Per-account view with change history and snapshot timeline

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python 3.11+ / FastAPI |
| Frontend | Next.js 16 / TypeScript / Tailwind CSS |
| Database | SQLite (SQLAlchemy ORM) |
| Scheduler | APScheduler |
| Scraper | Instaloader / Mock mode |

## Quick Start

### Backend
```bash
cd backend
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings \
    "python-jose[cryptography]" bcrypt python-multipart apscheduler aiosmtplib \
    httpx email-validator
cp ../.env.example .env
python -m uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:3000 in your browser.

### Docker
```bash
docker-compose up --build
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for the interactive API documentation.

## Project Structure

```
insta_tracker/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI application
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # Database setup
│   │   ├── deps.py           # Dependency injection
│   │   ├── models/           # SQLAlchemy models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   │   ├── scraper/      # Instagram scraping (mock + real)
│   │   │   ├── diff_engine.py
│   │   │   ├── snapshot_service.py
│   │   │   └── notification_service.py
│   │   └── scheduler/        # Background job scheduling
│   └── tests/                # pytest test suite
├── frontend/
│   └── src/
│       ├── app/              # Next.js pages
│       ├── components/       # React components
│       └── lib/              # API client, auth, utilities
├── docker-compose.yml
├── CLAUDE.md
└── .env.example
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | - | JWT signing key |
| `DATABASE_URL` | `sqlite:///./insta_tracker.db` | Database connection string |
| `SCRAPER_MODE` | `mock` | `mock` for development, `instaloader` for production |
| `SMTP_HOST` | `localhost` | SMTP server for email notifications |
| `FRONTEND_URL` | `http://localhost:3000` | Frontend URL for CORS |
