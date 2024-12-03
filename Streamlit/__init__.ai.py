import streamlit as st
from renderers import first_page

# Set page configuration
st.set_page_config(
    page_title="__init__.ai",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
        .main {
            background: linear-gradient(to bottom, #1E1F26, #343A40);
            color: #FFFFFF;
            font-family: 'Arial', sans-serif;
        }
        .title-text {
            font-size: 3.5rem;
            font-weight: bold;
            color: #E94F37;
            text-align: center;
        }
        .subtitle-text {
            font-size: 1.5rem;
            color: #FFC857;
            text-align: center;
            margin-bottom: 30px;
        }
        .feature-box {
            background: #343A40;
            padding: 20px;
            border-left: 5px solid #FF4B4B;
            border-radius: 10px;
            box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.2);
            margin: 10px 0;
            font-size: 1.2rem;
            margin-bottom: 2rem;
        }
        .start-button {
            font-size: 1.2rem;
            background-color: #E94F37;
            color: #000;
            border: none;
            text-decoration: none;
            padding: 15px 30px;
            border-radius: 5px;
            text-align: center;
            display: inline-block;
            margin: 20px auto;
        }
        .start-button:hover {
            background-color: #FFC857;
            color: #000;
        }
    </style>
""",
    unsafe_allow_html=True,
)

def get_started():
    st.session_state['current_page'] = "page_1"
    st.switch_page('pages/Init_Chat.py')
    st.rerun()

# Page Header
def render_welcome_page():
    
    # Title Section
    st.markdown(
        "<div class='title-text'>Welcome to __init__.ai 🚀</div>", unsafe_allow_html=True
    )
    st.markdown(
        "<div class='subtitle-text'>Transform your ideas into fully functional projects in minutes!</div>",
        unsafe_allow_html=True,
    )

    # Description Section
    st.text(
        """
        Imagine a world where your ideas are translated into fully operational projects without the hassle of manual coding.
        __init__.ai does exactly that! Here's how:
    """
    )

    # Features Section
    col1, col2 = st.columns(2, gap="large")
    with col1:
        st.markdown(
            "<div class='feature-box'>1️. <b>Gather Requirements:</b> </br> Share your vision, and we’ll take care of the rest.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='feature-box'>2️. <b>Process Requirements:</b> </br> Using advanced AI, we refine and understand your needs.</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            "<div class='feature-box'>3️. <b>Create Folder Structure:</b> </br> Generate a professional-grade project scaffold.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<div class='feature-box'>4️. <b>Generate Entire Project:</b> </br> Receive production-ready code tailored to your requirements.</div>",
            unsafe_allow_html=True,
        )
    
    if st.button('Get Started', use_container_width=True):
        get_started()

    # Footer Section
    st.markdown(
        """
        ---
        <div style='text-align: center; font-size: 0.9rem;'>
            Powered by कल्प AI • Built for Creators and Innovators ✨
        </div>
    """,
        unsafe_allow_html=True,
    )

    

if 'current_page' not in st.session_state:
    st.session_state['current_page'] = "welcome_page"  # Default page

if st.session_state['current_page'] == 'welcome_page':
    render_welcome_page()

if st.session_state['current_page'] == "page_1":
    first_page.render_first_page()

if st.session_state['current_page'] == "stack_suggestion":
    stack_suggestion_page.render_stack_suggestions()
    
    
