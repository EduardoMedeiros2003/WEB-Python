from pydantic import BaseModel, Field

class LoginPayload(BaseModel):
    username: str
    password: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    id: str = Field(..., alias='_id')
    username: str