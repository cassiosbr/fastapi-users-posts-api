from app.repositories.user_repository import UserRepository
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

class UserService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, db, name: str, email: str, password: str):

        if not name or not email:
            raise ValueError("Nome e email são obrigatórios")
        
        if len(name) > 100:
            raise ValueError("O nome deve ter no máximo 100 caracteres")
        
        if len(password.encode("utf-8")) > 72:
            raise ValueError("Senha muito longa. Máximo permitido: 72 bytes.")
        
        if self.get_user_by_email(db, email):
            raise ValueError("Email já existe")
        
        return self.user_repository.create(db, name, email, pwd_context.hash(password))
    
    def get_all_users(self, db):
        return self.user_repository.get_all_users(db)

    def get_user_by_id(self, db, user_id: int):
        user = self.user_repository.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("Usuário não encontrado")
        return user
    
    def get_user_by_email(self, db, email: str):
        user = self.user_repository.get_user_by_email(db, email)
        if not user:
            return None
        return user
    
    def authenticate_user(self, db, email: str, password: str):
        user = self.get_user_by_email(db, email)
        if not user:
            return False
        if not pwd_context.verify(password, user.hashed_password):
            return False
        return user
