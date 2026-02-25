from types import SimpleNamespace
from unittest.mock import Mock
from app.services.user_service import UserService

def test_create_user():
    mock_db = Mock()
    mock_repo = Mock()
    mock_repo.get_user_by_email.return_value = None  # Simula email não existente
    mock_repo.create.return_value = SimpleNamespace(id="18e5c07f28274019b154248d41be3f18", name="Test User", email="test@example.com")

    service = UserService(mock_repo)
    user = service.create_user(db=mock_db, name="Test User", email="test@example.com", password="password123")
    
    assert user.id == "18e5c07f28274019b154248d41be3f18"
    assert user.name == "Test User"
    assert user.email == "test@example.com"

def test_create_user_with_existing_email():
    mock_db = Mock()
    mock_repo = Mock()
    
    mock_repo.get_user_by_email.return_value = SimpleNamespace(id="18e5c07f28274019b154248d41be3f18", name="Existing User", email="existing@example.com")
    service = UserService(mock_repo)

    try:
        service.create_user(db=mock_db, name="New User", email="existing@example.com", password="password123")
    except ValueError as e:
        assert str(e) == "Email já existe"