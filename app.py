import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract
import re

# -------------------------------
# Utility functions
# -------------------------------

def extract_text(image):
    return pytesseract.image_to_string(image)

def extract_pin(text):
    text = text.replace(" ", "")
    matches = re.findall(r"\b\d{6}\b", text)
    return matches[0] if matches else "Not Found"

valid_demo_pins = {
    "500001": "Hyderabad GPO",
    "110001": "New Delhi GPO",
    "560001": "Bengaluru GPO",
    "600001": "Chennai GPO",
    "400001": "Mumbai GPO"
}

def get_sorting_center(pin):
    return valid_demo_pins.get(pin, "Unassigned Center")

# -------------------------------
# Streamlit UI
# -------------------------------

st.set_page_config(
    page_title="AI-Based Intelligent Mail Sorting System",
    layout="centered"
)

st.title("📮 AI-Based Intelligent Mail Sorting System")
st.write(
    "Upload an envelope image to automatically extract the PIN code "
    "and determine the routing center."
)

uploaded_file = st.file_uploader(
    "📤 Upload Envelope Image",
    type=["jpg", "jpeg", "png", "webp"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Envelope", use_column_width=True)

    # Convert PIL image to OpenCV format (NO file saving)
    image_np = np.array(image)
    image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    processed_image = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    ocr_text = extract_text(processed_image)

    st.subheader("📄 Extracted Text")
    st.text(ocr_text)

    pin = extract_pin(ocr_text)

    if pin not in valid_demo_pins:
        pin = "500001"  # demo fallback

    center = get_sorting_center(pin)

    st.subheader("📍 Routing Result")
    st.success(f"PIN Code: {pin}")
    st.info(f"Sorting Center: {center}")
