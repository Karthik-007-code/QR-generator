from jose import jwt, JOSEError
from fastapi import HTTPException
from dotenv import load_dotenv
import datetime
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
ALGORITHMN = os.getenv("ALGORITHMN")
exp_time = os.getenv("JWT_EXPIRE_TIME", "60")

def create_jwt_token(user):
    try:
        email = getattr(user, "email", None) or (user.get("email") if isinstance(user, dict) else getattr(user, "username", None))
        payload = {
            "email": email,
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(minutes=int(exp_time)) 
        }
        token = jwt.encode(payload, secret_key, algorithm=ALGORITHMN)
        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except JOSEError as e:  
        raise HTTPException(
            status_code=401,
            detail=str(e))