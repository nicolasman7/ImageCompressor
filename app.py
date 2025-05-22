import streamlit as st
from PIL import Image
from io import BytesIO
import os
import zipfile

MAX_DIM = 2000
MAX_SIZE = 2 * 1024 * 1024
SUPPORTED_FORMATS = ('.jpg', '.jpeg', '.png')

def resize_and_compress(image_file):
    img = Image.open(image_file).convert("RGB")
    img.thumbnail((MAX_DIM, MAX_DIM))
    buffer = BytesIO()

    low, high = 10, 95
    while low <= high:
        mid = (low + high) // 2
        buffer.seek(0)
        buffer.truncate()
        img.save(buffer, format='JPEG', quality=mid, optimize=True)
        if buffer.tell() <= MAX_SIZE:
            low = mid + 1
        else:
            high = mid - 1

    return buffer

# Streamlit app starts here
st.markdown("""
    <h1 style="text-align:center;">🗜️ Image Compressor</h1>
    <p style="text-align:center;">
        Click the button to upload images. They will be resized (max 2000x2000) and compressed (max 2MB).
    </p>
""", unsafe_allow_html=True)

uploaded_files = st.file_uploader("Choose image(s)", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

if st.button("Compress Images") and uploaded_files:
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file in uploaded_files:
            compressed = resize_and_compress(file)
            file_name = f"compressed_{file.name}"
            zipf.writestr(file_name, compressed.getvalue())

    st.success(f"{len(uploaded_files)} image(s) compressed!")

    st.download_button(
        label="Download All as ZIP",
        data=zip_buffer.getvalue(),
        file_name="compressed_images.zip",
        mime="application/zip"
    )
elif uploaded_files:
    st.warning("Click the 'Compress Images' button to start.")
