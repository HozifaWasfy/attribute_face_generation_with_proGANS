from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import torch
from PIL import Image
from model import Generator
import config
import random, os
from torchvision.utils import save_image
import time, json


def laod_generator(file_path, model):
    model_state = torch.load(file_path, map_location=config.DEVICE)
    model.load_state_dict(model_state["state_dict"])

gen = Generator(config.Z_DIM, config.IN_CHANNELS, img_channels=config.CHANNELS_IMG).to(config.DEVICE)

laod_generator("./generator.pth",gen)
gen.eval()


def get_user_with_key(key):
    with open("users.json", "r") as file:
        users = json.load(file)["users"]
    for user in users:
        if key in user["api_keys"]:
            return user
    return None

def get_user_with_username(uname):
    with open("users.json", "r") as file:
        users = json.load(file)["users"]
    for user in users:
        user_name = user["email"].split("@")[0]
        if uname in user_name:
            return user
    return None



def generate_image(gen, lattent_vector, user):
    curr_path = os.getcwd()
    user_images_dir = os.path.join(curr_path, f"{user['email']}_generated_faces")
    if not os.path.exists(user_images_dir):
        os.mkdir(user_images_dir)
    with torch.no_grad():
        images = gen(lattent_vector, 1.0, 6)
        image_path = os.path.join(user_images_dir, f"{time.time()}_face.png")
    save_image(images,image_path)
    return image_path
    
    
def generate_image_with_key(key, num_img):
    user = get_user_with_key(key)
    if user:
        l_vector = torch.randn(num_img,config.Z_DIM,1,1)
        img = generate_image(gen,l_vector,user)
        return img
    else:
        raise HTTPException(status_code=403, detail="unauthorizes")

# generate_image_with_key("apikey1_user2")

# with open("users.json", "r") as f:
#     data = json.load(f)
#     print(data)


# class user(BaseModel):
#     username: str
#     password: str

class lattent_request(BaseModel):
    lattent_vector: list

app = FastAPI()


# @app.post("/login")
# async def login():
#     pass


@app.get("/api/v1/generate_photo")
def generate(api_key: str, num_imgs: int):
    if num_imgs == 0:
        raise HTTPException(status_code=503, detail="cannot generate 0 images")
    img_name =  generate_image_with_key(api_key, num_imgs)
    # with open(img_name,"rb") as img:
    return FileResponse(path=img_name,media_type="image/png")