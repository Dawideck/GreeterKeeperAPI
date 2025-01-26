from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from fastapi import Depends, HTTPException, status
from data_models import User, UserInDB
from data.mock_data import mock_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")    
    
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail = "Invalid authentication credentials!",
                            headers = {"WWW-Authenticate": "Bearer"})
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="INactive user")
    return current_user

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    
def fake_decode_token(token):
    user = get_user(mock_db, token)
    return user
    
    
def mock_hash_password(password: str): # TODO let's implement some algorithm for a gist of security
    return "lolol" + password


