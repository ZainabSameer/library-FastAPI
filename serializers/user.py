from pydantic import BaseModel , ConfigDict

class UserSchema(BaseModel):
    username: str
    email: str
    password: str

    #class Config:
    #    orm_mode = True
    model_config = ConfigDict(
        from_attributes=True  # Update to use from_attributes
    )

class UserResponseSchema(BaseModel):
    username: str
    email: str

class UserLogin(BaseModel):
    username: str
    password: str  
class UserToken(BaseModel):
    token: str
    message: str

    model_config = ConfigDict(
        from_attributes=True  
    )
