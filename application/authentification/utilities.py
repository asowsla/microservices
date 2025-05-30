from datetime import datetime, timedelta, timezone
import bcrypt
import jwt
from typing import Optional, Union
from application.core.config import SETTINGS


# encoding JWT token
def encode_jwt(
    payload: dict,
    private_key: str = SETTINGS.JWT.private_key_path.read_text(),
    algorithm: str = SETTINGS.JWT.algorithm,
    expire_minutes: int = SETTINGS.JWT.access_token_expire_minutes,
    expire_timedelta: Optional[timedelta] = None,
) -> str:
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    expire = now + (expire_timedelta if expire_timedelta 
                    else timedelta(minutes=expire_minutes))
    
    to_encode.update({
        'exp': expire,
        'iat': now
    })
    
    return jwt.encode(
        to_encode,
        private_key,
        algorithm=algorithm
    )


# decoding JWT token
def decode_jwt(
    token: Union[str, bytes],
    public_key: str = SETTINGS.JWT.public_key_path.read_text(),
    algorithm: str = SETTINGS.JWT.algorithm,
) -> dict:
    return jwt.decode(
        token,
        public_key,
        algorithms=[algorithm]
    )


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


# validation of hash password
def validate_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )