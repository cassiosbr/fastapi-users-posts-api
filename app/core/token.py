from jose import jwt
from app.core.config import settings


def decode_token(token: str) -> str:
    payload = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    email: str = payload.get("sub")
    user_id = payload.get("id")
    return {"email": email, "id": user_id}
