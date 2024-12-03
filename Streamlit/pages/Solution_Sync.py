import os
import shutil
import streamlit as st
from utils.generate_project_utils import (
    extract_pdf_content,
    extract_fields_with_llm,
    generate_folder_structure,
    create_project_files,
    create_zip_and_download,
    display_project_structure,
)
from utils.github_utils import commit_and_push, git_wrapper

# Set page configuration
st.set_page_config(
    page_title="__init__.ai",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("## Upload your ideas, download your solution.")
st.markdown("##### – seamless project management made easy!")

# Upload PDF File
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:

    with st.spinner("Processing PDF..."):

        # Load PDF using PyPDF2
        pdf_text = extract_pdf_content(uploaded_file)
    st.success("PDF processed successfully.")

    # Loader and success message for LLM field extraction
    with st.spinner("Processing requirements..."):
        llm_output = extract_fields_with_llm(pdf_text)
    st.success("Requirements processed successfully.")

    # Loader and success message for folder structure generation
    with st.spinner("Generating folder structure..."):
        folder_structure = generate_folder_structure(pdf_text, llm_output)
        try:
            display_folder_structure = display_project_structure(
                folder_structure.get("output")
            )
        except:
            print("Error in displaying folder structure")

        folder_description = folder_structure.get("description")
        folder_structure = folder_structure.get("output")
    st.success("Folder structure generated successfully.")
    if folder_structure:
        st.write(display_folder_structure)

    # Generate project files using LLM
    project_files = create_project_files(folder_structure, pdf_text, folder_description)

    # Create a ZIP file and provide download link
    with st.spinner("Preparint your zip,"): 
        create_zip_and_download(project_files)

    # base_directory = folder_structure[0].split("/")[0]
    # st.write(base_directory)

    @st.fragment()
    def fragment_git():
        if st.button("Commit and Push to GitHub"):
            with st.spinner("Committing and pushing to GitHub..."):
                git_wrapper(project_files)
                # shutil.rmtree(base_directory)
            st.success("Files committed and pushed to GitHub successfully.")
    fragment_git()
    
else:
    st.info("Please upload a PDF file to proceed.")
