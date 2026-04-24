from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")