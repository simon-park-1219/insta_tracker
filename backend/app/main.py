from contextlib import asynccontextmanager

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.routers import auth, accounts, changes, notifications, settings as settings_router
from app.scheduler.jobs import run_scheduled_snapshots

scheduler = BackgroundScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Start scheduler
    scheduler.add_job(run_scheduled_snapshots, "interval", minutes=10, id="snapshot_job")
    scheduler.start()

    yield

    # Shutdown
    scheduler.shutdown()


app = FastAPI(
    title="InstaTracker API",
    description="Instagram Follower/Following Tracker MVP",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url, "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(changes.router)
app.include_router(notifications.router)
app.include_router(settings_router.router)


@app.get("/api/health")
def health_check():
    return {"status": "ok"}
