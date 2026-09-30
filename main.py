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
from auth.jwt import create_jwt_token
from auth.dependenct import  has_access,get_current_user
from DB.get_user_email import get_user_db


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
def login(request:Request,email:str = Depends(get_current_user)):
    if email:
        return templates.TemplateResponse(name="dashboard.html", request=request)
    else:
        return templates.TemplateResponse(name="login.html", request=request)
    


@app.get("/signup", response_class=HTMLResponse)
def signup(request:Request,email:str = Depends(get_current_user)):
    if email:
        return templates.TemplateResponse(name="dashboard.html", request=request)
    else:
        return templates.TemplateResponse(name="sign-up.html", request=request)
    

@app.get("/dashboard",response_class=HTMLResponse)
def dashboard(request:Request,email:str = Depends(get_current_user)):
    if email is None :
        return templates.TemplateResponse(name="login.html", request=request)
    else:
        current_user=get_user_db(email)
        if current_user["status"] == status.HTTP_200_OK:
            return templates.TemplateResponse("dashboard.html", {
                "request":request,
                "user":current_user
            })
        else:
            return templates.TemplateResponse(name="login.html", request=request)

    

@app.post("/signup")
async def signup_post(request: Request,response:Response):
    form_data = await request.form()
    try:
        # Validate raw form dictionary through your Pydantic schema
        user = UserCreate(**form_data)
        user.password = hash_password(user.password)
        token=create_jwt_token(user)

        response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,     
        secure=True,        
        samesite="strict",  
        max_age=3600,       
        path="/"           
        )
        
        user_insert = insertion(user)
        if user_insert["status"] == status.HTTP_201_CREATED:
            return templates.TemplateResponse("dashboard.html", {
                "request": request,
                "message": user_insert["message"],
            })
        

    except ValidationError as e:
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
    

   
    
