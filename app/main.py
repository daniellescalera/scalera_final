from builtins import Exception
from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.database import Database
from app.dependencies import get_settings
from app.routers import user_routes
from app.routers.analytics_routes import router as analytics_router
from app.utils.api_description import getDescription
from app.models import user_model

app = FastAPI(
    title="User Management",
    description=getDescription(),
    version="0.0.1",
    contact={
        "name": "API Support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
)

# Routers correctly included
app.include_router(user_routes.router)
app.include_router(analytics_router)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    settings = get_settings()
    Database.initialize(settings.database_url, settings.debug)

    async with Database._engine.begin() as conn:
        await conn.run_sync(user_model.Base.metadata.create_all)

# Global exception handler (optional - currently commented out)
