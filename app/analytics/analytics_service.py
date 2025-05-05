from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.user_model import User

async def get_user_retention(db: AsyncSession):
    # Total number of users (signups)
    total_signups_result = await db.execute(select(func.count()).select_from(User))
    total_signups = total_signups_result.scalar()

    # Returning users = users whose updated_at is different from created_at
    returning_users_result = await db.execute(
        select(func.count()).select_from(User).where(User.updated_at != User.created_at)
    )
    returning_users = returning_users_result.scalar()

    # Calculate retention rate
    retention_rate = (returning_users / total_signups) * 100 if total_signups > 0 else 0

    return {
        "total_signups": total_signups,
        "returning_users": returning_users,
        "retention_rate": round(retention_rate, 2)
    }
