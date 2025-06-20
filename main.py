import streamlit as st
from rembg import remove
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import io
import base64
import numpy as np

MAX_SIZE = (300, 300)

def apply_magical_filter(image, filter_type):
    if filter_type == "Invert Colors":
        return ImageOps.invert(image.convert("RGB"))
    elif filter_type == "Blur":
        return image.filter(ImageFilter.BLUR)
    elif filter_type == "Sharpen":
        return image.filter(ImageFilter.SHARPEN)
    elif filter_type == "Enhance":
        return ImageEnhance.Contrast(image).enhance(2.0)
    elif filter_type == "Comic Book":
        return ImageOps.posterize(image, 3)
    elif filter_type == "Glitch":
        return ImageOps.solarize(image)
    return image



def removebg(img_file):
    try:
        input_image = Image.open(img_file).convert("RGBA")
        input_image.thumbnail(MAX_SIZE)
        output_image = remove(input_image)
        output_image.thumbnail(MAX_SIZE)
        return output_image
    except Exception as e:
        st.error(f"❌ Background removal error: {e}")
        return None

def get_image_download_link(image, filename="output.png"):
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    b64 = base64.b64encode(buffer.getvalue()).decode()
    return f'<a href="data:file/png;base64,{b64}" download="{filename}">📥 Download Output Image</a>'

def main():
    st.set_page_config(page_title="🧙 Magical Image Editor", page_icon="✨", layout="wide")
    st.title("🎨 Magical Image Editor — Unleash Your Imagination!")

    uploaded_file = st.file_uploader("📤 Upload an Image", type=["jpg", "jpeg", "png"])

    if 'upload_count' not in st.session_state:
        st.session_state.upload_count = 0

    st.sidebar.title("ℹ️ About")
    st.sidebar.markdown("""
Magical Image Editor is a simple tool to remove image backgrounds and apply fun visual effects.

- ⚙️ Powered by AI
- 🎨 Instant transparent PNGs
- 🧪 Experimental filters
""")
    st.sidebar.markdown(f"**Images Processed:** `{st.session_state.upload_count}`")

    if uploaded_file:
        st.session_state.upload_count += 1
        st.info("⏳ Processing image...")

        result = removebg(uploaded_file)

        if result:
            st.success("✅ Background removed successfully!")

            col1, col2 = st.columns(2)
            with col1:
                st.subheader("📷 Original")
                image = Image.open(uploaded_file).convert("RGBA")
                image.thumbnail(MAX_SIZE)
                st.image(image, width=MAX_SIZE[0])

            with col2:
                st.subheader("🌟 No Background")
                st.image(result, width=MAX_SIZE[0])

            st.sidebar.markdown("### ✅ Download")
            st.sidebar.markdown(get_image_download_link(result), unsafe_allow_html=True)

            st.sidebar.markdown("### ✨ Apply Filter")
            if st.sidebar.checkbox("Enable Filters"):
                filter_type = st.sidebar.selectbox("🎆 Choose Filter", [
                    "Invert Colors", "Blur", "Sharpen", "Enhance", "Comic Book", "Glitch"
                ])
                filtered_img = apply_magical_filter(result, filter_type)
                st.image(filtered_img, caption=f"{filter_type} Effect", width=MAX_SIZE[0])
                
if __name__ == "__main__":
    main()

# To Run:
# python -m streamlit run main.py
