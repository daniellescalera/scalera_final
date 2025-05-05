from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user_model import User, UserRole
from app.utils.nickname_generator import generate_nickname
from app.utils.security import hash_password

class UserService:

    @staticmethod
    async def register_user(db: AsyncSession, user_data: dict, email_service) -> User:
        if not user_data.get("email") or not user_data.get("password"):
            raise HTTPException(status_code=400, detail="Email and password are required.")

        existing_user = await db.execute(select(User).where(User.email == user_data["email"]))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already exists.")

        if not user_data.get("nickname"):
            user_data["nickname"] = generate_nickname(user_data["email"])

        role_value = user_data.get("role", "AUTHENTICATED")
        try:
            role = UserRole(role_value)
        except ValueError:
            role = UserRole.AUTHENTICATED

        new_user = User(
            email=user_data["email"],
            nickname=user_data["nickname"],
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            role=role,
            hashed_password=hash_password(user_data["password"]),
            is_professional=user_data.get("is_professional", False),
        )

        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)

        await email_service(new_user, new_user.verification_token)
        return new_user

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: str) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(db: AsyncSession, user_id: str, user_data: dict) -> User:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found.")

        for key, value in user_data.items():
            setattr(user, key, value)

        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: str) -> bool:
        user = await UserService.get_user_by_id(db, user_id)
        if not user:
            return False

        await db.delete(user)
        await db.commit()
        return True

    @staticmethod
    async def list_users(db: AsyncSession, skip: int = 0, limit: int = 10):
        result = await db.execute(select(User).offset(skip).limit(limit))
        users = result.scalars().all()
        total = await db.scalar(select(func.count()).select_from(User))

        return {
            "items": users,
            "total": total,
            "page": skip // limit + 1,
            "size": limit
        }

    @staticmethod
    async def login_for_access_token(db: AsyncSession, email: str, password: str):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not user.verify_password(password):
            raise HTTPException(status_code=401, detail="Incorrect email or password.")
        if user.is_locked:
            raise HTTPException(status_code=400, detail="Account locked due to too many failed login attempts.")
        if not user.email_verified:
            raise HTTPException(status_code=401, detail="Please verify your email address before logging in.")
        return user

    @staticmethod
    async def verify_email_with_token(db: AsyncSession, user_id: str, token: str) -> bool:
        user = await UserService.get_user_by_id(db, user_id)
        if not user or user.verification_token != token:
            return False
        user.verify_email()
        await db.commit()
        return True

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_nickname(db: AsyncSession, nickname: str) -> User:
        result = await db.execute(select(User).where(User.nickname == nickname))
        return result.scalar_one_or_none()
