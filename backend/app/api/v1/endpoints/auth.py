"""Routes for auth module."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.exceptions import UserAlreadyExists
from app.schemas.auth import UserIn, UserOut, Token
from app.services.auth import (
    create_user,
    authenticate_user,
    generate_access_token,
)

router = APIRouter(
    tags=['auth'],
)


@router.post(
    '/register',
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserIn,
) -> UserOut:
    """User registration."""
    try:
        created_user = await create_user(user)
    except UserAlreadyExists as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists.",
        ) from error

    return created_user


@router.post(
    '/login',
    response_model=Token,
    status_code=status.HTTP_200_OK,
)
async def login(
    credentials: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """User authentication."""
    user = await authenticate_user(credentials)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password.",
        )

    return await generate_access_token(user)
