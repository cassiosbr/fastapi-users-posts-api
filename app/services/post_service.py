from app.repositories.post_repository import PostRepository


class PostService:

    def __init__(self, post_repository: PostRepository):
        self.post_repository = post_repository

    def create_post(self, db, title: str, content: str, user_id: int):

        if not title or not content:
            raise ValueError("Título e conteúdo são obrigatórios")
        
        if len(title) > 100:
            raise ValueError("O título deve ter no máximo 100 caracteres")
        
        return self.post_repository.create(db, title, content, user_id)
    
    def get_all_posts(self, db):
        return self.post_repository.get_all_posts(db)

    def get_post_by_id(self, db, post_id: int):
        post = self.post_repository.get_post_by_id(db, post_id)
        if not post:
            raise ValueError("Post não encontrado")
        return post
    
    def get_posts_by_user_id(self, db, user_id: int):
        posts = self.post_repository.get_posts_by_user_id(db, user_id)
        if not posts:
            return []
        return posts

