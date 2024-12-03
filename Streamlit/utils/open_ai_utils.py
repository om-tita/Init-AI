import openai
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv


# Load the OpenAI API key from environment variables
load_dotenv()  # Load environment variables from the .env file
openai.api_key = os.getenv("OPENAI_API_KEY")

# Utility for Chat-based Completion (e.g., GPT-4 chat completion API)
def get_chat_completion(
    messages: List[Dict[str, str]],
    model: str = "gpt-4o-mini",
    max_tokens: int = 1500,
) -> Optional[str]:
    """
    Generate a chat completion response based on message history.

    Args:
        messages (List[Dict[str, str]]): A list of messages in the format [{"role": "user/system/assistant", "content": "<message>"}]
        model (str): The model to use, e.g., "gpt-4"
        max_tokens (int): The maximum number of tokens in the response
        **kwargs: Additional parameters for the OpenAI API

    Returns:
        Optional[str]: The assistant's response or None if there's an error
    """
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            # response_format={ "type": "json_object" },
            temperature=0.0,
            # response_format = {"type": "json_object"},
            # max_tokens=max_tokens,
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def format_chat_message(role: str, content: str) -> Dict[str, str]:
    """
    Format a chat message for the OpenAI API.

    Args:
        role (str): The role of the message sender, "user", "assistant", or "system"
        content (str): The content of the message

    Returns:
        Dict[str, str]: A formatted message dictionary
    """
    return {"role": role, "content": content}


def get_ai_response(session_messages, model="gpt-3.5-turbo"):
    """
    Fetches the AI response from OpenAI's API.

    Parameters:
        session_messages (list): Session state messages to be formatted 
                                 for OpenAI API in the form of 
                                 [{"role": "user", "content": "message content"}].
        model (str): The OpenAI model to use for generating responses.
    
    Returns:
        str: The complete response from the AI model.
    """
    # Format messages for OpenAI API
    formatted_messages = [
        {"role": message["role"], "content": message["content"]}
        for message in session_messages
    ]
    
    # Initialize the full response
    full_response = ""
    
    # Stream the response
    for response in openai.chat.completions.create(
        model=model,
        messages=formatted_messages,
        stream=True,
    ): 
        delta_content = (response.choices[0].delta.content if response.choices else "")
        if delta_content:  # Only concatenate if delta_content is not None
            full_response += (
                delta_content  # Add a blinking cursor to simulate typing
            )
    return full_response
