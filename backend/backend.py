from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.responses import FileResponse
import torch, os
from backend_utils import *
from backend_schemas import *
from db_crud import get_user_by_username, create_user
from db_engine import SessionLocal, Base, engine
from backend_config import config

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db = get_db()
app = FastAPI()


@app.post("/api/v1/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db , form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/api/v1/add_user")
async def add_user_to_db(user: UserOnSubmit, db: Session = Depends(get_db)):
    userdb = user.copy()
    userdb.password = hash_password(user.password)
    user =  create_user(db, userdb)
    os.mkdir(os.path.join(os.getcwd(), user.content_directory))
    return user
    
    

@app.get("/users/me/", response_model=UserBase)
async def read_users_me(current_user: oauth2_scheme = Depends(get_current_user)):
    return UserBase(username=current_user.username,email=current_user.email, full_name=current_user.full_name)

@app.post("/api/v1/generate_photo")
def generate(num_imgs: int, labels: label_vector, current_user: oauth2_scheme = Depends(get_current_user), db = Depends(get_db)):
    labels = torch.tensor(labels.attributes, dtype=torch.float32).to(config.DEVICE)
    if num_imgs == 0:
        raise HTTPException(status_code=503, detail="cannot generate 0 images")
    img_name =  generate_save_image(num_imgs, labels, current_user.username, db)
    return FileResponse(path=img_name,media_type="image/png")
    

            
        