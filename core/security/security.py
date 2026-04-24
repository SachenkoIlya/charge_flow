from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from cryptography.fernet import Fernet
from passlib.context import CryptContext
from jose import JWTError, ExpiredSignatureError
from core.security.config import settings
from jose import jwt
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()


class Security:
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
    if ENCRYPTION_KEY:
        cipher = Fernet(ENCRYPTION_KEY)
    else:
        raise ValueError("ENCRYPTION_KEY not found in .env file!")
    
    pwd_context = CryptContext(
        schemes=['bcrypt'],
        
    )

    @staticmethod
    def _normalize_password(password: str) -> bytes:
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def hashed_password(self, password: str):
        """Хэширование пароля"""
        password = self._normalize_password(password)
        return self.pwd_context.hash(password)

    def very_password(self, password: str, hashed: str):
        """Проверка пароля"""
        password = self._normalize_password(password)
        return self.pwd_context.verify(password, hashed)
    

    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Создание access токена"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({
            "exp": expire,  "iat": datetime.now(timezone.utc)
        })
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    

    def create_refresh_token(self, data: dict) -> str:
        """Создание refresh токена"""
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        """Декодирование токена"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        except ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token expired")
        except JWTError:
            raise HTTPException(status_code=401, detail="Invalid token")    

    def encrypt_data(self, text: str) -> str:
        return self.cipher.encrypt(text.encode()).decode()

    def decrypt_data(self, encrypted_text: str) -> str:
        return self.cipher.decrypt(encrypted_text.encode()).decode()

security = Security()