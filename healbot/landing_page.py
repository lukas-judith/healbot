import streamlit as st
from PIL import Image

# Set the page configuration
st.set_page_config(page_title="RehabWise", page_icon=":hospital:")

# Custom CSS to center the content
st.markdown(
    """
    <style>
    .centered-content {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        height: 100vh;
    }
    .logo {
        width: 150px;
        height: auto;
    }
    .enter-button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin-top: 20px;
        cursor: pointer;
        border: none;
        border-radius: 5px;
    }
    .enter-button:hover {
        background-color: #45a049;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Centered content
st.markdown('<div class="centered-content">', unsafe_allow_html=True)

# Display the logo
logo_path = r"C:\Users\jorge\OneDrive\Documents\Work\RehabWise\healbot\healbot\logo.png"
logo = Image.open(logo_path)
st.image(logo, caption="RehabWise", use_column_width=False, class_="logo")

# Display the button
if st.button("Enter", key="enter", help="Click to enter the application"):
    st.write("Welcome to RehabWise!")

st.markdown('</div>', unsafe_allow_html=True)
