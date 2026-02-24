from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.schemas.post import PostCreate, PostResponse
from app.services.post_service import PostService
from app.repositories.post_repository import PostRepository
from app.db.session import get_db

from app.models.user import User
from app.core.security import get_current_user


router = APIRouter(prefix="/posts", tags=["posts"])

def get_post_repository():
    return PostRepository()

def get_post_service(repo: PostRepository = Depends(get_post_repository)):
    return PostService(repo)

@router.post("/", response_model=PostResponse)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db),
    service: PostService = Depends(get_post_service),
    current_user: User = Depends(get_current_user)
):
    try:
        print(f"Criando posts para o usuário: {current_user.name} (ID: {current_user.id})")
        return service.create_post(db, post.title, post.content, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[PostResponse])
def get_all_posts(db: Session = Depends(get_db), service: PostService = Depends(get_post_service), current_user: User = Depends(get_current_user)):
    print(f"Listando todos os posts para o usuário: {current_user.name} (ID: {current_user.id})")
    return service.get_all_posts(db)