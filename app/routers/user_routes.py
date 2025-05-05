from fastapi import APIRouter, Depends, HTTPException, Response, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
from app.services.jwt_service import create_access_token
from app.services.email_service import get_email_service
from app.services.user_service import UserService
from app.schemas.token_schemas import TokenResponse
from app.schemas.user_schemas import UserBase, UserCreate, UserListResponse, UserResponse, UserUpdate, PaginatedUserResponse
from app.dependencies import get_db, oauth2_scheme, require_role
from app.schemas.pagination_schema import generate_pagination_links
from app.settings.config import get_settings

router = APIRouter()
settings = get_settings()

@router.get("/users/{user_id}", response_model=UserResponse, tags=["User Management Requires (Admin or Manager Roles)"])
async def get_user(user_id: str, session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    user = await UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(user)

@router.put("/users/{user_id}", response_model=UserResponse, tags=["User Management Requires (Admin or Manager Roles)"])
async def update_user(user_id: str, user_update: UserUpdate, session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    user_data = user_update.dict(exclude_unset=True)
    updated_user = await UserService.update_user(session, user_id, user_data)
    if not updated_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return UserResponse.from_orm(updated_user)

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["User Management Requires (Admin or Manager Roles)"])
async def delete_user(user_id: str, session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN"]))):
    success = await UserService.delete_user(session, user_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/users/", response_model=PaginatedUserResponse, tags=["User Management Requires (Admin or Manager Roles)"])
async def list_users(request: Request, skip: int = 0, limit: int = 10, session: AsyncSession = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN", "MANAGER"]))):
    paginated_response = await UserService.list_users(session, skip, limit)
    return paginated_response

@router.post("/users/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, tags=["User Management Requires (Admin or Manager Roles)"])
async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_db), email_service=Depends(get_email_service), token: str = Depends(oauth2_scheme), current_user: dict = Depends(require_role(["ADMIN"]))):
    created_user = await UserService.create(session, user_data.dict(), email_service)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create user")
    return UserResponse.from_orm(created_user)

@router.post("/register/", response_model=UserResponse, tags=["Login and Registration"])
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_db), email_service=Depends(get_email_service)):
    try:
        new_user = await UserService.register_user(session, user_data.dict(), email_service)
        return UserResponse.from_orm(new_user)
    except IntegrityError:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists.")
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login/", response_model=TokenResponse, tags=["Login and Registration"])
async def login(form_data: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_db)):
    user = await UserService.login_for_access_token(session, form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": str(user.id), "role": user.role.name},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/verify-email/{user_id}/{token}", status_code=status.HTTP_200_OK, tags=["Login and Registration"])
async def verify_email(user_id: str, token: str, session: AsyncSession = Depends(get_db)):
    success = await UserService.verify_email_with_token(session, user_id, token)
    if not success:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired verification token")
    return {"message": "Email verified successfully."}
