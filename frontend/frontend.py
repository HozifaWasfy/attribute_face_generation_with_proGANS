import streamlit as st
import requests
import os
from PIL import Image
from io import BytesIO
import json
# api_key = os.environ["FACE_API_KEY"]

USER_NAME = "hoz"
PASSWORD = "password"
def auth_user(username, password):
    api_url = f"http://localhost:8000/api/v1/token"
    data = {"username": username, "password": password}
    response = requests.post(api_url, data=data, auth=requests.auth.HTTPBasicAuth(data["username"], data["password"]))
    
def get_image_from_api(key, labels, num_imgs):
    api_url = f"http://localhost:8000/api/v1/generate_photo?num_imgs={num_imgs}"
    load = json.dumps({
        "attributes": labels
    })
    imgs = requests.post(api_url, data=load, )
    print(imgs.json)
    return BytesIO(imgs.content)





attribute_dict = {
            '5_o_Clock_Shadow':0,
            'Bald':1, 
            'Bangs':2,
            'Black_Hair':3,
            'Blond_Hair':4,
            'Brown_Hair':5,
            'Eyeglasses': 6,
            'Goatee':7,
            'Gray_Hair':8, 
            'Male':9,
            'Mustache':10,
            'No_Beard':11,
            'Sideburns':12,
            'Straight_Hair':13,
            'Wavy_Hair':14,
            'Wearing_Hat':15,
            'Young':16
               }

def get_attrib_from_choices(
        hair_color_choice,
        hair_style_choice,
        beard_style,
        age,
        male_radio,
        glasses,
        bangs,
        hat
        ):
    labels = [-1] * 17
    hair_color_choice = hair_color_choice.replace(" ", "_")
    hair_style_choice = hair_style_choice.replace(" ", "_")
    beard_style = beard_style.replace(" ", "_")
    yes_or_no = lambda x : -1 if x == "No" else 1
    labels[attribute_dict[hair_color_choice]] = 1
    labels[attribute_dict[hair_style_choice]] = 1
    labels[attribute_dict[beard_style]] = 1
    
    labels[attribute_dict["Young"]] = -1 if age == "Old" else 1
    labels[attribute_dict["Bangs"]] = yes_or_no(bangs)
    labels[attribute_dict["Wearing_Hat"]] = yes_or_no(hat)
    labels[attribute_dict["Eyeglasses"]] = yes_or_no(glasses)
    labels[attribute_dict["Male"]] = 1 if male_radio == "Male" else -1

    return labels



# Dropdown menu options
hair_color = ["Black Hair", "Brown Hair", "Blond Hair", "Gray Hair"]
hair_style = ["Straight Hair", "Wavy Hair", "Bald"]
beard = ["Mustache", "No Beard", "Goatee", "5 oClock Shadow","Sideburns"]
age = ["Young", "Old"]

# Function to display image based on selected options
def display_image(labels, num_imgs):
    # Add logic here to determine the image path based on selected options
    # For simplicity, using a placeholder image
    key = "apikey1_user1"

    image_path = get_image_from_api(key, labels, num_imgs)
    st.image(image_path, caption="Selected Image", use_column_width=True)

# Streamlit UI
st.title("Attribute based face generation")
sidebar_tab = st.sidebar.radio("Select Mode", ["Transfere Learning", "Generate Image"])
# Dropdown menus

if sidebar_tab == "Generate Image":
    st.sidebar.header("Choose Your face features")
    num_images = st.sidebar.number_input("Number of faces", min_value=1, step=1)
    hair_color_choice = st.sidebar.selectbox("Hair Color", hair_color)
    hair_style_choice = st.sidebar.selectbox("Hair Style", hair_style)
    beard_style = st.sidebar.selectbox("Beard Style", beard)
    age = st.sidebar.selectbox("Age", age)
    male_radio = st.sidebar.radio("Gender", options=["Male","Female"])
    glasses = st.sidebar.radio("Glasses", options=["Yes", "No"])
    bangs = st.sidebar.radio("Bangs", options=["Yes", "No"])
    hat = st.sidebar.radio("Wearing Hat", options=["Yes", "No"])

    attributes = get_attrib_from_choices(
        hair_color_choice,
        hair_style_choice,
        beard_style,
        age,
        male_radio,
        glasses,
        bangs,
        hat
        )


    st.title(attributes)
    if st.button("Display Image"):
        display_image(attributes, num_images)

# Tab 2 content
elif sidebar_tab == "Transfere Learning":
    pass
    st.sidebar.header("Tab 2 Options")
