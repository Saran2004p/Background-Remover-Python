import streamlit as st
from rembg import remove
from PIL import Image
import io
import base64
import numpy as np

def removebg(img, threshold):
    input_image = Image.open(img)
    return remove(input_image, threshold=threshold)

def main():
    st.set_page_config(
        page_title="✨ Magical Background Remover",
        page_icon="🚀",
        layout="wide"
    )

    st.title("Remove Backgrounds with a Wave of Your Wand! 🪄🌈")

    uploaded_file = st.file_uploader("Upload Your Image 📷", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.sidebar.title("🛠️ Image Controls")
        threshold = st.sidebar.slider("Background Removal Sensitivity", 0, 255, 150)

        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True, channels="RGB")
        st.info("Processing... 🎩✨")

        result = removebg(uploaded_file, threshold)
        st.image(result, caption="Voila! Background Removed 🌟", use_column_width=True, channels="RGBA")

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

        # Replace the GIF with your desired GIF URL
        st.sidebar.image("https://media.giphy.com/media/3o7bue3JMFz1qoNSac/giphy.gif", use_column_width=True)

        # Add a playful quote
        st.sidebar.markdown("### 🎉 Feeling magical? Keep experimenting and have fun! 🌟")

if __name__ == '__main__':
    main()
