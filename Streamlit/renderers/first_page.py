import streamlit as st
from services import DescriptionPreProcessingService

description_pre_processing_service = DescriptionPreProcessingService()

def render_first_page():
    with st.form("initial_req_form"):
        st.title("Glad to see you! Let's get going")
        st.markdown("Enter title and description of your project, so we can help you.")
        # Add two text input fields
        first_field = st.text_input("Project title:")
        second_field = st.text_area("Project description:")

        # Add a submit button
        submitted = st.form_submit_button("Submit")
        if submitted:
            with st.spinner("Analysing description..."):
                st.session_state['project_title'] = first_field
                result =  description_pre_processing_service.description_pre_processing(first_field, second_field)

                st.session_state['initial_requirements'] = result
                
                st.switch_page('pages/page_3.py')