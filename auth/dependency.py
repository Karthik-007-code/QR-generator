from fastapi import Request
from jose import jwt, JOSEError
from dotenv import load_dotenv
import os

load_dotenv()
secret_key = os.getenv("SECRET_KEY")
ALGORITHMN = os.getenv("ALGORITHMN")

async def get_current_user(request: Request) -> str | None:
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        return None

    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHMN])
        email = payload.get("email")
        return email
    except JOSEError:
        return None


