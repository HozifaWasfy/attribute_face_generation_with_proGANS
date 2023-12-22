from pydantic import BaseModel
import datetime 

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str or None = None


class UserBase(BaseModel):
    username: str
    email: str or None = None
    full_name: str or None = None

class UserOnSubmit(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str
    content_directory: str
    created_at: datetime.datetime
    class config:
        orm_model = True
    

# class ImageInDB(BaseModel):
#     id: int or None = None
#     num_faces: int
#     name: str
#     noise: bytes
#     attributes: bytes
#     created_at: datetime.datetime or None = None
    
#     class config:
#         orm_model = True

class ImageInDB(BaseModel):
    id: int or None = None
    num_faces: int
    name: str
    noise: str
    attributes: str
    created_at: datetime.datetime or None = None
    
    class config:
        orm_model = True

class label_vector(BaseModel):
    attributes : list[float]