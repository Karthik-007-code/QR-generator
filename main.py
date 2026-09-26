from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from qrcode import make
from fastapi import status
from fastapi.templating import Jinja2Templates
from fastapi import Request

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
    

# @app.post("/login",username=username,password=password)
# def login_post(username:str,password:str):
   
    
