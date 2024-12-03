import openai
import streamlit as st
from utils.generate_project_utils import (
    create_project_files,
    create_zip_and_download,
    display_project_structure,
    extract_fields_with_llm,
    generate_folder_structure,
)
from utils.github_utils import commit_and_push, git_wrapper
from utils.open_ai_utils import get_chat_completion

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "summary" not in st.session_state:
    st.session_state.summary = ""

if "is_chatting" not in st.session_state:
    st.session_state.is_chatting = True  # Keep chat visible initially


def chat_prompt():
    return """
    You are a chatbot specialized in gathering product requirements and technical specifications.
    for software development. Ask questions about the project, its features, and technical constraints.
    Do not introduce new information or make assumptions. If information is unclear, ask for clarification.
    Do not ask for personal information or any sensitive data.
    Do not ask very detailed questions about the project.
    Help the user to provide the necessary information for the project.
    """


def summarize_chat(messages):
    chat_transcript = ""

    print("summarize_chat.....")
    print("hello message = ", messages)
    # Constructing the chat transcript
    for message in messages:
        chat_transcript += f"{message['role']}: {message['content']}\n"

    # Simulate the system and user prompts
    system_prompt = f"""
        You are a specialized AI assistant trained to gather, validate, and summarize product requirements and technical specifications for software development projects. Your focus is to ensure the capture of accurate, well-structured, and contextually relevant information regarding project features, technical constraints, and client expectations. If information is incomplete or ambiguous, explicitly request clarification.
    """

    user_prompt = f""" Context: You are assisting in creating chat conversations aimed at gathering and summarizing product requirements. Your task is to generate a structured and accurate product requirements document based on the given conversation.
            Instructions:  
            1. Extract and prioritize all key points relevant to project features, constraints, and objectives.  
            2. Validate consistency across the conversation for coherence and avoid introducing unverified information.  
            3. If any ambiguity is present in the transcript, mark it clearly for follow-up.  
            4. Use concise, professional, and structured language.
            5. Only use the chat transcript to generate the product requirements document do not add anything or do not anything by your end.
            6. if not enough information is present in the chat transcript, reply with no sufficient details found.

            Here is the chat transcript:  
            {chat_transcript}

            Deliverable: A clearly formatted product requirement document adhering to the provided instructions.
        """

    message_to_send = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Getting the response from OpenAI API (using the utility function)
    response = get_chat_completion(message_to_send, st.session_state["openai_model"])
    st.session_state.summary = response  # Save the summary in session state
    print("generated successfully")
    return response

st.markdown("### Innovation Starts with a Conversation...")

if st.session_state.is_chatting:
    # Chat Page (Visible by default)
    def render_chat(messages):
        for message in messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Render existing chat history
    if st.session_state.messages:
        render_chat(st.session_state.messages)

    # User input for chat
    if prompt := st.chat_input("What is up?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
        # Display assistant message in chat message container
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            message_to_send = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]
            message_to_send.append(
                {
                    "role": "system",
                    "content": chat_prompt(),
                }
            )
            # Simulate stream of response with milliseconds delay
            for response in openai.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=message_to_send,
                stream=True,
            ):
                # Get content in response, checking for None
                delta_content = (
                    response.choices[0].delta.content if response.choices else ""
                )
                if delta_content:  # Only concatenate if delta_content is not None
                    full_response += delta_content
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
            st.session_state.messages.append(
                {"role": "assistant", "content": full_response}
            )

    # Button to Summarize Chat
    if (len(st.session_state.messages) > 0):
        if st.button("Summarize Chat"):
            st.session_state.is_chatting = False  # Hide chat component
            st.rerun()

elif not st.session_state.is_chatting:
    # Summary Page (Visible after summarizing the chat)
    with st.spinner("Summarizing chat..."):
        summary = summarize_chat(st.session_state.messages)
        st.session_state.summary = summary

    st.success("Chat summarized successfully.")
    st.markdown("#### AI generated product requirements:")
    st.markdown(summary)

    # Loader and success message for LLM field extraction
    with st.spinner("Processing requirements..."):
        llm_output = extract_fields_with_llm(summary)
    st.success("Requirements processed successfully.")

    # Loader and success message for folder structure generation
    with st.spinner("Generating folder structure..."):
        folder_structure = generate_folder_structure(summary, llm_output)
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
    project_files = create_project_files(folder_structure, summary, folder_description)

    # Create a ZIP file and provide download link
    with st.spinner("Preparing your zip,"):
        create_zip_and_download(project_files)


    if st.button("Commit and Push to GitHub"):
        with st.spinner("Committing and pushing to GitHub..."):
            git_wrapper(project_files)
            # shutil.rmtree(base_directory)
        st.success("Files committed and pushed to GitHub successfully.")
        