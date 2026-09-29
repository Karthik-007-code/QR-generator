from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from qrcode import make
from fastapi import status
from fastapi.templating import Jinja2Templates
from fastapi import Request
from DB.models import UserCreate
from utility.Hashing import hash_password
from pydantic import ValidationError
from DB.insert import insertion

app = FastAPI(title="QR-code Generater")

templates = Jinja2Templates(directory="templets")



# routes
@app.get("/")
def root():
    return {"Title":"QR-code Generator",
           "status":status.HTTP_200_OK,
           "End-point":"/",
           "documentation":"/docs"
           }


@app.get("/login", response_class=HTMLResponse)
def login(request:Request):
    return templates.TemplateResponse(name="login.html", request=request)

@app.get("/signup", response_class=HTMLResponse)
def signup(request:Request):
    return templates.TemplateResponse(name="sign-up.html", request=request)
    
@app.post("/signup")
async def signup_post(request: Request):
    form_data = await request.form()
    try:
        # Validate raw form dictionary through your Pydantic schema
        user = UserCreate(**form_data)
        user.password = hash_password(user.password)
        # Save user to DB here...
        
        return insertion(user)

    except ValidationError as e:
        # Extract user-friendly error message
        error_msg = e.errors()[0]["msg"]
        return templates.TemplateResponse(
            "sign-up.html",
            {
                "request": request,
                "error": error_msg,
                "fullname": form_data.get("fullname", ""),
                "email": form_data.get("email", ""),
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    
# @app.post("/login",username=username,password=password)
# def login_post(username:str,password:str):
   
    
