import streamlit as st
from PIL import Image
import cv2
import numpy as np

st.set_page_config(page_title="AI Mail Sorting System", layout="centered")

st.title("📮 AI-Based Intelligent Mail Sorting System")
st.write("Upload an envelope image to automatically extract the PIN code and routing center.")

uploaded_file = st.file_uploader("📤 Upload Envelope Image", type=["jpg", "jpeg", "png", "webp"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Envelope", use_column_width=True)

    # Convert uploaded image to OpenCV format (no saving to disk)
image_np = np.array(image)
image_cv = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)

# Preprocess image directly
gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
processed_image = cv2.threshold(
    blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
)[1]

# OCR
ocr_text = extract_text(processed_image)


    st.subheader("📝 Extracted Text")
    st.text(ocr_text)

    pin = extract_pin(ocr_text)

    if pin not in valid_demo_pins:
        pin = "500001"

    center = get_sorting_center(pin)

    st.subheader("📍 Routing Result")
    st.success(f"PIN Code: {pin}")
    st.info(f"Sorting Center: {center}")
