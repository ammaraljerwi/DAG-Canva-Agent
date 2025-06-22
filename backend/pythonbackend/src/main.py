from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.database.database import create_db_and_tables

from src.api.v1.endpoints import agents, auth, messages, users

from .core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
app.include_router(messages.router, prefix="/api/v1/messages", tags=["messages"])
app.include_router(agents.router, prefix="/api/v1/agents", tags=["messages"])


CANVA_APP_ID = settings.CANVA_APP_ID

# IMPORTANT: Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",  # Your Canva SDK frontend's development server port
    "http://localhost:3001",
    "https://app-{}.canva-apps.com".format(CANVA_APP_ID.lower()),
    "*",
    # Add any other origins where your Canva app might be running (e.g., specific IPs)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "hello from python"}
