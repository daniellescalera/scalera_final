from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.dependencies import get_db
from app.analytics.analytics_service import get_user_retention

router = APIRouter(
    prefix="/analytics",
    tags=["analytics"]
)

@router.get("/retention", summary="Get user retention analytics")
async def user_retention(db: AsyncSession = Depends(get_db)):
    retention_data = await get_user_retention(db)
    return retention_data
