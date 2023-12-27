from db_data_models import *
from backend_schemas import *
from sqlalchemy.orm import Session
from datetime import datetime

def create_user(db: Session, user: UserOnSubmit):
    hashed_password = user.password
    db_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        content_directory= user.username,
        )
        
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user



def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_images_by_owner(db: Session, user_id: int):
    return db.query(Images).filter(Images.user_id == user_id).all()

def get_image_by_id(db: Session, img_id: int):
    return db.query(Images).filter(Images.id == img_id).first()
    
def create_image(db: Session, image: ImageInDB, user_id: int):
    image_in_db = Images(
        name = image.name,
        noise = image.noise,
        attributes = image.attributes,
        user_id = user_id , 
        num_faces = image.num_faces
    )
    db.add(image_in_db)
    db.commit()
    db.refresh(image_in_db)
    return image_in_db