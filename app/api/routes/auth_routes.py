from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token
from app.db.session import get_db
from app.repositories.user_repository import UserRepository
from app.services.user_service import UserService


router = APIRouter(prefix="/auth", tags=["auth"])


def get_user_repository():
    return UserRepository()

def get_user_service(repo: UserRepository = Depends(get_user_repository)):
    return UserService(repo)

@router.post("/login")
def login(
    db=Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service)
):
    email = form_data.username
    password = form_data.password
    user = service.authenticate_user(db, email, password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )
    access_token = create_access_token(
        data={"sub": user.email, "id": user.id}
    )
    return {"access_token": access_token, "token_type": "bearer"}
