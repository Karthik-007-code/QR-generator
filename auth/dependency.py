from jose import jwt
from jose.exceptions import JOSEError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
ALGORITHMN = os.getenv("ALGORITHMN")
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        payload = jwt.decode(credentials.credentials,secret_key,algorithms=[ALGORITHMN])
        email = payload.get("email")
        if email is None:
           return None
        return email
    except JOSEError as e:
        raise HTTPException(
            status_code=401,
            detail=str(e))

