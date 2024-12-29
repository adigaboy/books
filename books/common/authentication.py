
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from common.config import config

security = HTTPBasic()

def get_current_username(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
):
    current_username_bytes = credentials.username
    correct_username_bytes = config['DEFAULT'].get('ADMIN_USERNAME')
    is_correct_username = current_username_bytes == correct_username_bytes
    current_password_bytes = credentials.password
    correct_password_bytes = config['DEFAULT'].get('ADMIN_PASSWORD')
    is_correct_password = current_password_bytes == correct_password_bytes
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
