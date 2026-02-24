from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.db.session import get_db

from app.models.user import User

from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository():
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db), service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        return service.create_user(db, user.name, user.email, user.password)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/", response_model=list[UserResponse])
def get_all_users(db: Session = Depends(get_db), service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    print('listando todos os usuários')
    return service.get_all_users(db)

    # list comprehension
    # users = service.get_all_users(db)
    # return [
    #     UserResponse(id=user.id, name=user.name, email=user.email)
    #     for user in users
    # ]

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), service: UserService = Depends(get_user_service), current_user: User = Depends(get_current_user)):
    try:
        return service.get_user_by_id(db, user_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))