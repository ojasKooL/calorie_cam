from dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import google.generativeai as genai
from PIL import Image

# Configure the API key for Google Generative AI
api_key = os.getenv("GEMINI_API")
if not api_key:
    raise ValueError("GEMINI_API key not found in environment variables")
genai.configure(api_key=api_key)

def get_gemini_response(input_text, image_parts, prompt):
    model = genai.GenerativeModel("gemini-pro-vision")
    response = model.generate_content([input_text, image_parts[0], prompt])
    return response.text

def input_image_setup(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")

input_prompt = """
You are an expert in nutrition where you need to see the food items from the image and calculate the total calories, also provide the details of every food item with calories intake in the below format:

1. Item 1 - number of calories
2. Item 2 - number of calories
----
----
"""

st.set_page_config(page_title="Calorie Cam")
st.header("Calorie Cam")

input_text = st.text_input("Input Prompt: ", key="input")
uploaded_file = st.file_uploader("Upload Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

submit = st.button("Tell me the total calories")

if submit:
    if uploaded_file is not None and input_text:
        image_parts = input_image_setup(uploaded_file)
        response = get_gemini_response(input_text, image_parts, input_prompt)
        st.write(response)
    else:
        st.error("Please provide both the input prompt and an image.")
