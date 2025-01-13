from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.v1.dependencies import get_user_interactor, get_user_repo
from app.core.security import create_access_token, get_current_user_id
from app.interactors.user import UserCreateDTO, UserInteractor, UserUpdateDTO
from app.repositories.user import UserRepository


router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=dict)
async def register(
    user_data: UserCreateDTO,
    interactor: UserInteractor = Depends(get_user_interactor),
):
    """Register new user if it not already exists in db"""
    try:
        return await interactor.create_user(user_data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    interactor: UserInteractor = Depends(get_user_interactor),
):
    """Authenticate user with login and password"""
    user = await interactor.authenticate(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )

    access_token = create_access_token(
        data={"sub": str(user["id"])},
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("/me")
async def get_current_user(
    current_user_id: int = Depends(get_current_user_id),
    repo: UserRepository = Depends(get_user_repo),
):
    """Get info about authenticated user"""
    user = await repo.get_by_id(current_user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/me")
async def update_me(
    user_data: UserUpdateDTO,
    current_user_id: int = Depends(get_current_user_id),
    interactor: UserInteractor = Depends(get_user_interactor),
):
    """Update authenticated user`s info"""
    return await interactor.update_user(current_user_id, user_data)
