import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import base64
import numpy as np
import requests

# Function to apply magical filters
def apply_magical_filter(image, filter_type):
    if filter_type == "Invert Colors":
        if image.mode == "RGBA":
            image = image.convert("RGB")
        return ImageOps.invert(image)
    elif filter_type == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    elif filter_type == "Enhance":
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(2.0)  # Adjust the enhancement factor as needed
    elif filter_type == "Comic Book":
        return ImageOps.posterize(image, 3)
    elif filter_type == "Glitch":
        return ImageOps.solarize(image)
    else:
        return image  # Default to original image

# Function to generate a random quote
def get_random_quote():
    quotes = [
        "Why fit in when you were born to stand out? - Dr. Seuss",
        "The more you like yourself, the less you are like anyone else, which makes you unique. - Walt Disney",
        "Be yourself; everyone else is already taken. - Oscar Wilde",
        "Don't cry because it's over, smile because it happened. - Dr. Seuss",
        "Life is what happens when you're busy making other plans. - Allen Sanders",
        "You are never too old to set another goal or to dream a new dream. - C.S. Lewis"
    ]
    return np.random.choice(quotes)

# Function to remove background
def removebg(img, threshold):
    input_image = Image.open(img)
    return remove(input_image, threshold=threshold)

def main():
    st.set_page_config(
        page_title="✨ Magical Image Editor",
        page_icon="🎨",
        layout="wide"
    )

    st.title("Unleash Your Creativity with Magical Effects! 🎩✨")

    uploaded_file = st.file_uploader("Upload Your Image 📷", type=["jpg", "jpeg", "png"])

    # Counter for uploaded images
    if 'upload_count' not in st.session_state:
        st.session_state.upload_count = 0
    st.sidebar.markdown(f"Uploaded Images: {st.session_state.upload_count}")

    if uploaded_file is not None:
        st.session_state.upload_count += 1
        st.sidebar.title("🛠️ Image Controls")
        threshold = st.sidebar.slider("Background Removal Sensitivity", 0, 255, 150)

        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True, channels="RGB")
        st.info("Processing... 🚀✨")

        result = removebg(uploaded_file, threshold)
        st.image(result, caption="Background Removed 🌟", use_column_width=True, channels="RGBA")

        st.success("✨ Background magically removed! Explore more options below.")

        # Display original and processed images side by side
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Image", use_column_width=True, channels="RGB")

        with col2:
            st.image(result, caption="Processed Image", use_column_width=True, channels="RGBA")

        # Download the processed image
        result_image = Image.fromarray(np.array(result))
        result_bytes = io.BytesIO()
        result_image.save(result_bytes, format='PNG')
        result_b64 = base64.b64encode(result_bytes.getvalue()).decode()
        st.sidebar.markdown(
            f"### 📥 Download Your Masterpiece [here](data:application/octet-stream;base64,{result_b64})",
            unsafe_allow_html=True
        )

        # Add a playful GIF animation
        st.sidebar.image("https://media.giphy.com/media/3ohjV4udF1r1dMWvc4/giphy.gif", use_column_width=True)

        # Add a random quote
        st.sidebar.markdown("### 📜 Random Quote:")
        st.sidebar.text(get_random_quote())

        # Button to apply magical filters
        if st.sidebar.button("Apply Magical Filters 🧙‍♂️"):
            filter_type = st.sidebar.selectbox("Choose a Magical Filter", ["Invert Colors", "Blur", "Sharpen", "Enhance", "Comic Book", "Glitch"])
            st.image(apply_magical_filter(result, filter_type), caption=f"{filter_type} Effect Applied 🌈", use_column_width=True, channels="RGBA")

    # Toggle between light and dark mode
    dark_mode = st.sidebar.checkbox("Dark Mode 🌙")
    if dark_mode:
        st.markdown("""<style>
                    body { background-color: #121212; color: #FFFFFF }
                    </style>""", unsafe_allow_html=True)
    else:
        st.markdown("""<style>
                    body { background-color: #FFFFFF; color: #000000 }
                    </style>""", unsafe_allow_html=True)

if __name__ == '__main__':
    main()
