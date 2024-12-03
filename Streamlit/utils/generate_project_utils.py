from utils.open_ai_utils import get_chat_completion
import json
import os
import streamlit as st
from PyPDF2 import PdfReader
import os
import zipfile
import io
import shutil


@st.fragment()
def create_zip_and_download(project_files):
    """
    Creates a ZIP file of the project files and returns a downloadable link.
    """
    with st.spinner("Preparing your ZIP file..."):

        # Create a temporary directory to store the files
        temp_dir = "/tmp/project_files"
        os.makedirs(temp_dir, exist_ok=True)

        # Save the project files to the temporary directory
        for file in project_files:
            file_path = os.path.join(temp_dir, file["file_path"])
            os.makedirs(
                os.path.dirname(file_path), exist_ok=True
            )  # Create directories if they don't exist

            # Write the file content to the path
            with open(file_path, "w") as f:
                f.write(file["file_content"])

        # Create a ZIP file from the saved project files
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for foldername, subfolders, filenames in os.walk(temp_dir):
                for filename in filenames:
                    file_path = os.path.join(foldername, filename)
                    arcname = os.path.relpath(
                        file_path, temp_dir
                    )  # Relative path inside the zip
                    zip_file.write(file_path, arcname=arcname)

        zip_buffer.seek(0)

    st.success("ZIP file created successfully.")

    if st.download_button(
        label="Download Project as ZIP",
        data=zip_buffer,
        file_name="project.zip",
        mime="application/zip",
    ):
        st.success("ZIP file downloaded successfully.")

    # Clean up the temporary directory using shutil.rmtree
    shutil.rmtree(temp_dir)


def extract_pdf_content(pdf_path):
    """
    Extracts text from a PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def extract_fields_with_llm(pdf_content, project_title=None):
    """
    Uses an LLM to extract 'tech_stack' and 'base_path' from the PDF content.
    """
    project_title_string = ""

    if project_title:
        project_title_string = f"Project Title is {project_title}"

    user_prompt = f"""
    Analyze the following PDF content and extract the values for:
    1. tech_stack: The technology stack mentioned in the content.
    2. base_path: will be the name of application it should be in the camlecase.
    If either of these values is not explicitly mentioned, respond with 'Not Provided'.
    
    PDF content:
    {pdf_content}
    
    {project_title_string}
    """

    system_prompt = (
        "You are a helpful assistant for analyzing text and extracting details."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    output = get_chat_completion(messages=messages)
    # st.write(output)
    return output


def generate_file_content(file_path, project_description, folder_description):
    """
    Generates file content based on the given file path and project description using an LLM.
    """
    prompt = f"""
    Based on the following project description, generate the content for the specified file.
    Provide only the content of the file without any extra explanation.
    Only generate the given file path and do not include any additional files or directories.
    
    Project Description:
    {project_description}
    
    Folder Description (Use as context ONLY):
    {folder_description}

    File Path:
    {file_path}

    output format:
    {{
        "file_path": "{file_path}",
        "file_content": "..."
    }}

    NOTE: respond in the form of a JSON object otherwise app will crash.
    """

    system_prompt = "You are a helpful assistant for generating code."

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt},
    ]

    output = get_chat_completion(messages=messages)

    return output


def create_project_files(file_list, project_description, folder_description):
    """
    Creates the project files based on the provided file list and project description.
    """

    project = []

    for file_path in file_list:
        with st.spinner(f"Generating {file_path}..."):
            file_content = generate_file_content(
                file_path, project_description, folder_description
            )
        print("generated file content for", file_path)
        st.success(f"{file_path} generated successfully.")
        file_content = json.loads(file_content)
        project.append(
            {"file_path": file_path, "file_content": file_content.get("file_content")}
        )
        st.text(file_path)
        st.code(file_content.get("file_content"))

        # # Ensure directory exists
        # os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # # Optionally, write the content to files in the file system:
        # with open(file_path, "w") as file:
        #     file.write(file_content.get("file_content"))

    return project


def display_project_structure(project_files):

    user_prompt = f"""
    Generate a markdown representation of the project structure based solely on the provided file paths.
    Do not include any additional files or directories that are not explicitly listed in the input.
    Ensure that the structure is formatted cleanly and adheres strictly to the input.

    File Path List:
    {project_files}

    Expected Output Format:
    ```aiTextSummarizer/
    ├── main.py
    ├── utils/
    │   └── helpers.py
    ├── README.md
    └── .env```

    Input Example:
    project_files = [
        "aiTextSummarizer/main.py",
        "aiTextSummarizer/utils/helpers.py",
        "aiTextSummarizer/README.md",
        "aiTextSummarizer/.env",
    ]
    
    Example Output Format:
        ```
        aiTextSummarizer/
        ├── main.py
        ├── utils/
        │   └── helpers.py
        ├── README.md
        └── .env
        ```

    """

    messages = [
        {
            "role": "system",
            "content": "You are an AI assistant for formating project structures.",
        },
        {"role": "user", "content": user_prompt},
    ]

    output = get_chat_completion(messages=messages)
    return output


def generate_folder_structure(pdf_content, tech_stack):

    user_prompt = f""" 
    You are an AI assistant trained to generate structured folder hierarchies for software projects. 
    Based on the provided project description and technology stack, 
    create a well-organized folder structure. Include the following details:

    1. The **base_path** as the root folder.
    2. Relevant subfolders and files (e.g., `main.py`, `utils/helper.py`, `models/model.py`) appropriate for the specified tech stack.
    3. Essential files like `README.md` and an environment file (e.g., `.env` or `example.env` or `requirements.txt`).
    4. Ensure the folder structure is practical and consistent with the conventions of the provided tech stack.
    5. Don't include the path for folders only file names.
    6. Add one file for the project description and standard coding conventions.
    7. Add description of generated folder structure in the output which can use to generate code for added files.
    8. Do not include file for logo or any other image files.
    
    **Project Description:**
    {pdf_content}

    **Tech Stack Details:**
    {tech_stack}

    Output Format:
    {{"output": [
            "base_path/main.py", 
            "base_path/README.md", 
            "base_path/.env"
    ], "description": "Description of generated folder structure."}}

    NOTE: Respond in the form of a JSON array only, otherwise the app will crash. dont include ``` or anything else in response.
          Do not include file for logo or any other image files otherwise app will crash.
    """

    system_prompt = (
        "You are a helpful assistant for generating project folder structures."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    output = get_chat_completion(messages=messages)

    return json.loads(output)
