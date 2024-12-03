import logging
import streamlit as st
from pages.Solution_Sync import (
    create_project_files,
    create_zip_and_download,
    extract_fields_with_llm,
    generate_folder_structure,
)

# Initialize session states for messages if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Hello Could you please provide the functional requirement of the product?",
        }
    ]

if "current_product_data" not in st.session_state:
    st.session_state.current_product_data = {
        "functinal_requirement": "",
        "user_case": "",
        "programming_lauguage_with version": "",
        "frame_work_with version": "",
        "authentication_service": "",
        "user_management": "",
        "database_type": "",
        "DB_tool": "",
        "testing_library": "",
        "api_documetation": "",
        "deployment": "",
        "scalability": "",
        "security": "",
        "monitoring": "",
        "analytics": "",
        "error_reporting": "",
    }


def run_chatbot():
    try:
        if "initial_requirements" in st.session_state:
            st.success("Great! Please Provide us a few more details:")
            st.success(st.session_state["initial_requirements"])

        enhanced_description = st.text_area("Enhanced Description:")

        if st.button("Submit"):
            with st.spinner("Extracting fields with LLM..."):
                if "project_title" in st.session_state:
                    title = st.session_state["project_title"]
                llm_output = extract_fields_with_llm(
                    enhanced_description, title or None
                )
            st.success("Fields extracted successfully with LLM.")

            with st.spinner("Generating folder structure..."):
                folder_structure = generate_folder_structure(
                    enhanced_description, llm_output
                )
                st.write(folder_structure)
            st.success("Folder structure generated successfully.")

            # Generate project files using LLM
            project_files = create_project_files(folder_structure, enhanced_description)
            st.write(project_files)

            # Create a ZIP file and provide download link
            create_zip_and_download(project_files)

    except Exception as e:
        logging.error("Error occurred:", e)
        raise e


# Run the chatbot page
run_chatbot()
