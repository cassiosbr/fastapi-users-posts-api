from sqlalchemy.orm import Session
from app.models.post import Post

class PostRepository:

    @staticmethod
    def create(db: Session, title: str, content: str, user_id: int):
        post = Post(title=title, content=content, user_id=user_id)
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_post_by_id(db: Session, post_id: int):
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def get_all_posts(db: Session):
        return db.query(Post).all()

    @staticmethod
    def get_posts_by_user_id(db: Session, user_id: int):
        return db.query(Post).filter(Post.user_id == user_id).all()