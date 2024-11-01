from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="MULTILANGUAGE INVOICE EXTRACTOR", page_icon="🧾")

# Retrieve API key from environment and configure the API client
api_key = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate response from the model
def get_gemini_response(input, image_parts, prompt):
    if image_parts:
        response = model.generate_content([input, image_parts[0], prompt])
        return response.text
    else:
        return "No image data provided."

# Header and subtitle
st.title("📄 Multilanguage Invoice Extractor")
st.subheader("Extract information from invoices in various languages!")

# Sidebar for user instructions
with st.sidebar:
    st.markdown("### Instructions")
    st.write("1. Upload an invoice image in JPEG or PNG format.")
    st.write("2. Enter your prompt/question regarding the invoice.")
    st.write("3. Click the 'Submit' button to get the response.")

# Text input and file uploader
input_text = st.text_input("Enter your question or prompt:", key="input")
uploaded_file = st.file_uploader("Choose an image file:", type=["jpeg", "jpg", "png"])

def input_image_details(uploaded_file):
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
        st.warning("No file uploaded.")
        return []

# Display uploaded image if available
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice Image", use_column_width=True)

submit = st.button("Submit")

input_prompt = "You are an expert in understanding invoices. We will upload an invoice and you will have to answer questions regarding them."

if submit:
    if uploaded_file is not None:
        image_data = input_image_details(uploaded_file)
        if image_data:
            response = get_gemini_response(input_prompt, image_data, input_text)
            st.subheader("Response:")
            st.write(response)
        else:
            st.warning("Image data is empty.")
    else:
        st.warning("Please upload an image before submitting.")
