import os, torch
from torchvision.utils import save_image
import time, json
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from db_crud import get_user_by_username, Session, create_image
from db_data_models import Images, User
from passlib.context import CryptContext
from jose import JWTError, jwt
from io import BytesIO
from backend_config import config
from model import Generator
from backend_schemas import UserInDB, TokenData, ImageInDB
from db_engine import SessionLocal


SECRET_KEY = "83daa0256a2289b0fb23693bf1f6034d44396675749244721a2b20e896e11662"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
passwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

def load_generator(file_path, model):
    model_state = torch.load(file_path, map_location=config.DEVICE)
    model.load_state_dict(model_state["state_dict"])


gen = Generator(
        config.Z_DIM, config.IN_CHANNELS,config.ATTRIB_DIM, img_channels=config.CHANNELS_IMG
    ).to(config.DEVICE)
load_generator("generator-HQ-5.pth", gen)
gen.eval()

def hash_password(password_plain):
    return passwd_context.hash(password_plain)

def verify_password(plain, hashed):
    return passwd_context.verify(plain, hashed)

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False

    return user

def create_access_token(data: dict, expires_delta: timedelta or None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def generate_image_name(user: UserInDB):
    img_name = f"{time.time()}-face.png"
    noise_name = f"{time.time()}-noise.pt"
    labels_name = f"{time.time()}-labels.pt"
    path = os.path.join(os.getcwd(), user.content_directory)
    
    return img_name, noise_name , labels_name, path
    

def generate_save_image(num_imgs, labels, username, db: Session):
    
    labels = labels.repeat((num_imgs,1))
    noise = torch.randn((num_imgs, config.Z_DIM, 1, 1)).to(config.DEVICE)
    imgs = gen(noise, labels, 1.0, 5) *0.5 +0.5
    curr_user = get_user_by_username(db, username)
    img_name,noise_name, labels_name, path = generate_image_name(curr_user)
    save_image(imgs, os.path.join(path, img_name))
    # buff_nosie = BytesIO()
    # buff_labels = BytesIO()
    torch.save(labels,os.path.join(path, labels_name))
    torch.save(noise,os.path.join(path, noise_name))
    # buff_nosie.seek(0)
    # buff_labels.seek(0)
    image_in_db = ImageInDB(
        name = img_name,
        noise = noise_name,
        attributes = labels_name,
        num_faces = num_imgs,
    
    )
    # image_in_db = ImageInDB(
    #     name = img_name,
    #     noise = buff_nosie.read(),
    #     attributes = buff_labels.read(),
    #     num_faces = num_imgs
    # )
    create_image(db, image_in_db, curr_user.id)
    return os.path.join(path, img_name)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception

        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception

    user = get_user_by_username(SessionLocal(), token_data.username)
    if user is None:
        raise credential_exception

    return user
