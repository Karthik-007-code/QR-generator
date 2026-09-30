from fastapi import FastAPI, Depends, Response, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError

from DB.models import UserCreate, UserLogin
from DB.insert import insertion
from DB.get_user_email import get_user_db
from utility.Hashing import hash_password, verify_password
from auth.jwt import create_jwt_token
from auth.dependency import get_current_user


app = FastAPI(title="QR-code Generator")

templates = Jinja2Templates(directory="templets")
# routes
@app.get("/")
def root():
    return {
        "Title": "QR-code Generator",
        "status": status.HTTP_200_OK,
        "End-point": "/",
        "documentation": "/docs"
    }


@app.get("/login", response_class=HTMLResponse)
def login(request: Request, email: str | None = Depends(get_current_user)):
    if email:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("login.html", {"request": request})


@app.get("/signup", response_class=HTMLResponse)
def signup(request: Request, email: str | None = Depends(get_current_user)):
    if email:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return templates.TemplateResponse("sign-up.html", {"request": request})


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, email: str | None = Depends(get_current_user)):
    if not email:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    
    current_user_res = get_user_db(email)
    if current_user_res["status"] == status.HTTP_200_OK:
        return templates.TemplateResponse("dashboard.html", {
            "request": request,
            "user": current_user_res["user"],
            "message": "Successfully logged in"
        })
    else:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@app.post("/signup")
async def signup_post(request: Request):
    form_data = await request.form()
    try:
        user_create = UserCreate(**form_data)
        raw_password = user_create.password
        user_create.password = hash_password(raw_password)
        
        user_insert = insertion(user_create)
        if user_insert["status"] == status.HTTP_201_CREATED:
            token = create_jwt_token(user_create)
            response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
            response.set_cookie(
                key="access_token",
                value=token["access_token"],
                httponly=True,
                samesite="lax",
                max_age=3600,
                path="/"
            )
            return response
        else:
            return templates.TemplateResponse(
                "sign-up.html",
                {"request": request, "error": "Database error creating user"},
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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


@app.post("/login")
async def login_post(request: Request):
    form_data = await request.form()
    try:
        login_data = UserLogin(**form_data)
        identifier = login_data.username  # Email or Username input from form
        
        db_res = get_user_db(identifier)
        if db_res["status"] != status.HTTP_200_OK or not db_res["user"]:
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "error": "Account not found with this email/username.",
                    "username": identifier
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        db_user = db_res["user"]
        if not verify_password(login_data.password, db_user["password"]):
            return templates.TemplateResponse(
                "login.html",
                {
                    "request": request,
                    "error": "Invalid password.",
                    "username": identifier
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        token = create_jwt_token(db_user)
        response = RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(
            key="access_token",
            value=token["access_token"],
            httponly=True,
            samesite="lax",
            max_age=3600,
            path="/"
        )
        return response

    except ValidationError as e:
        error_msg = e.errors()[0]["msg"]
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": error_msg,
                "username": form_data.get("username", ""),
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )


@app.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(key="access_token", path="/")
    return response

    


    
