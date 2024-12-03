import os
import streamlit as st
from git import Repo
import shutil
import tempfile
import requests
from dotenv import load_dotenv

# Load the OpenAI API key from environment variables
load_dotenv()  # Load environment variables from the .env file

# GitHub Repo Info
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = os.getenv("REPO_NAME")
REPO_OWNER = os.getenv("REPO_OWNER")
REPO_URL = os.getenv("REPO_URL")


def initialize_git_repo(LOCAL_PROJECT_PATH):
    if not os.path.exists(LOCAL_PROJECT_PATH):
        os.makedirs(LOCAL_PROJECT_PATH)  # Create the directory if it doesn't exist
        st.write(f"Created directory: {LOCAL_PROJECT_PATH}")
    
    # Check if the folder is already a git repository
    if not os.path.exists(os.path.join(LOCAL_PROJECT_PATH, ".git")):
        st.write(f"Initializing Git repository in {LOCAL_PROJECT_PATH}")
        repo = Repo.init(LOCAL_PROJECT_PATH)  # Initialize a new git repo
        origin = repo.create_remote("origin", REPO_URL)  # Add the remote URL
    else:
        repo = Repo(LOCAL_PROJECT_PATH)  # Use existing repo
        origin = repo.remotes.origin if "origin" in repo.remotes else None

    return repo, origin

@st.fragment()
def commit_and_push(project_files):
    temp_dir = "/home/ec2-user/TC2024_Agni_KalpAI_Repo/Streamlit/tmp"

    os.makedirs(temp_dir, exist_ok=True)

    for file in project_files:
        file_path = os.path.join(temp_dir, file["file_path"])
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write(file["file_content"])

    LOCAL_PROJECT_PATH = "tmp"
    os.makedirs(LOCAL_PROJECT_PATH, exist_ok=True)  # Ensure the tmp directory exists

    repo, origin = initialize_git_repo(LOCAL_PROJECT_PATH)
    if not repo or not origin:
        st.error("Failed to initialize the Git repository.")
        shutil.rmtree(temp_dir)
        return

    try:
        repo.git.add(A=True)
        repo.index.commit("Initial commit")
        origin.push(refspec="master:master")  # Push to the master branch
        shutil.rmtree(temp_dir)  # Clean up
        st.success("Initial commit pushed to GitHub successfully.")
    except Exception as e:
        st.error(f"Error during push: {e}")
        shutil.rmtree(temp_dir)  # Clean up
        raise e


def git_wrapper(project_files):
    remote_ai = get_remote_url(REPO_OWNER, REPO_NAME, GITHUB_TOKEN)
    commit_to_remote_with_token(remote_ai, GITHUB_TOKEN, "Initial commit", project_files)



def get_remote_url(repo_owner, repo_name, token):
    """
    Fetch the HTTPS URL of a GitHub repository using the GitHub API.

    :param repo_owner: GitHub username or organization name.
    :param repo_name: Repository name.
    :param token: Personal access token for authentication.
    :return: Remote HTTPS URL of the repository.
    """
    api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json"
    }

    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        repo_data = response.json()
        return repo_data.get("clone_url")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def commit_to_remote_with_token(remote_url, token, commit_message, file_changes):
    """
    Clone a remote repo, commit changes, and push using a Git token.

    :param remote_url: The HTTPS URL of the remote repository.
    :param token: The personal access token for authentication.
    :param commit_message: Commit message for the changes.
    :param file_changes: Dictionary of file paths (relative to repo) and their content.
    """
    try:
        # Create a temporary directory to clone the repository
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Replace the URL with token-based authentication
            token_auth_url = remote_url.replace("https://", f"https://{token}@")
            
            print(f"Cloning repository to {tmp_dir}...")
            repo = Repo.clone_from(token_auth_url, tmp_dir)

            for change in file_changes:
                file_path = change["file_path"]
                file_content = change["file_content"]

                # Create directories and write the file
                file_full_path = os.path.join(tmp_dir, file_path)
                os.makedirs(os.path.dirname(file_full_path), exist_ok=True)
                with open(file_full_path, 'w') as f:
                    f.write(file_content)
                print(f"Updated file: {file_path}")

            # Stage and commit changes
            repo.git.add(all=True)
            repo.index.commit(commit_message)
            print("Changes committed.")

            # Push changes to the remote repository
            origin = repo.remote(name="origin")
            origin.push()
            print("Changes pushed successfully.")
            st.success("Files committed and pushed to GitHub successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")