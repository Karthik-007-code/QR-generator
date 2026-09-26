from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from qrcode import make
from fastapi import status

app = FastAPI(title="QR-code Generater")


# routes
@app.get("/")
def root():
    return {"Title":"QR-code Generator",
           "status":status.HTTP_200_OK,
           "End-point":"/",
           "documentation":"/docs"
           }


@app.get("/login",HTMLResponse=True)
def login():
    return HTMLResponse("templates/login.html")

@app.get("/signup",HTMLResponse=True)
def signup():
    return HTMLResponse("templates/sign-up.html")
    
# @app.post("/login",username=username,password=password)
# def login_post(username:str,password:str):
   
    
