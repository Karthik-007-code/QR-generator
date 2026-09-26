from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


EMAIL_REGEX = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"


class UserBase(BaseModel):
    """Base schema holding shared user attributes."""
    email: str = Field(
        ...,
        pattern=EMAIL_REGEX,
        description="User email address",
        examples=["user@example.com"],
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()


class User(UserBase):
    """
    Core User model representing stored user account credentials.
    """
    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique username",
    )
    password: str = Field(
        ...,
        min_length=6,
        description="User password (hashed in production)",
    )

    @field_validator("username")
    @classmethod
    def sanitize_username(cls, v: str) -> str:
        return v.strip()


class UserCreate(BaseModel):
    """
    Sign-up request schema matching templets/sign-up.html.
    """
    fullname: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Full name of the user",
    )
    email: str = Field(
        ...,
        pattern=EMAIL_REGEX,
        description="Valid email address",
    )
    password: str = Field(
        ...,
        min_length=6,
        description="Password (minimum 6 characters)",
    )
    confirm_password: Optional[str] = Field(
        default=None,
        description="Password confirmation",
    )

    @field_validator("email")
    @classmethod
    def normalize_email(cls, v: str) -> str:
        return v.strip().lower()

    @field_validator("fullname")
    @classmethod
    def sanitize_fullname(cls, v: str) -> str:
        return v.strip()

    @model_validator(mode="after")
    def verify_passwords_match(self):
        if self.confirm_password is not None and self.password != self.confirm_password:
            raise ValueError("Passwords do not match.")
        return self


class UserLogin(BaseModel):
    """
    Login request schema matching templets/login.html.
    Accepts either username or email.
    """
    username: str = Field(
        ...,
        min_length=1,
        description="Username or Email",
    )
    password: str = Field(
        ...,
        min_length=1,
        description="Account password",
    )
    remember: bool = Field(
        default=False,
        description="Remember user session",
    )

    @field_validator("username")
    @classmethod
    def sanitize_login_identifier(cls, v: str) -> str:
        return v.strip()


class UserResponse(BaseModel):
    """
    Public user profile schema excluding sensitive data (password).
    """
    id: Optional[int] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    email: str
    created_at: Optional[str] = None