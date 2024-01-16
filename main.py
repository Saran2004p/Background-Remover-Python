import streamlit as st
from rembg import remove
from PIL import Image
import io

def removebg(img):
    input_image = Image.open(img)
    return remove(input_image)

def main():
    st.title("Advanced Background Remover App")
    
    uploaded_file = st.file_uploader("Choose an Image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        st.sidebar.title("Image Controls")
        threshold = st.sidebar.slider("Background Removal Threshold", 0, 255, 150)
        
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        st.write("Processing...")

        result = removebg(uploaded_file)
        st.image(result, caption="Result", use_column_width=True)

        st.info("Adjust the threshold using the sidebar for better results.")

        # Display original and processed images side by side
        col1, col2 = st.beta_columns(2)
        with col1:
            st.image(uploaded_file, caption="Original Image", use_column_width=True)

        with col2:
            st.image(result, caption="Processed Image", use_column_width=True)

        # Download the processed image
        result_image = Image.fromarray(result)
        result_bytes = io.BytesIO()
        result_image.save(result_bytes, format='PNG')
        st.sidebar.markdown(
            f"### Download Processed Image [here](data:application/octet-stream;base64,{b64encode(result_bytes.getvalue()).decode()})",
            unsafe_allow_html=True
        )

if __name__ == '__main__':
    main()
